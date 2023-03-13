from dataclasses import dataclass, field
from elftools.dwarf.dwarf_expr import DWARFExprParser
from typing import Any, Self

@dataclass
class DwarfBaseType:
    name: str
    size: int


basetypes = {
    "uint8_t": DwarfBaseType("uint8_t", 1),
    "int8_t": DwarfBaseType("int8_t", 1),
    "uint16_t": DwarfBaseType("uint16_t", 2),
    "int16_t": DwarfBaseType("int16_t", 2),
    "uint32_t": DwarfBaseType("uint32_t", 4),
    "int32_t": DwarfBaseType("int32_t", 4),
    "uint64_t": DwarfBaseType("uint64_t", 8),
    "int64_t": DwarfBaseType("int64_t", 8),
    "float": DwarfBaseType("float", 4),
    "double": DwarfBaseType("double", 8),
    "bool": DwarfBaseType("bool", 1),
}


@dataclass
class DwarfMember:
    name: str
    offset: int
    datatype: Any = None

    @staticmethod
    def from_die(die):
        name = die.attributes["DW_AT_name"].value.decode("utf-8")
        parser = DWARFExprParser(die.cu.structs)
        op = parser.parse_expr(die.attributes["DW_AT_data_member_location"].value)
        if op[0].op_name != "DW_OP_plus_uconst":
            print("unknown member location type", op)
            return None
        return DwarfMember(name, op[0].args[0])


@dataclass
class DwarfArray:
    datatype: Any
    size: int
    dimensions: list[int] = field(default_factory=list)

    @staticmethod
    def get_dimensions(die):
        dimensions = []
        for c in die.iter_children():
            if c.tag != "DW_TAG_subrange_type":
                print("unexpected array child: ", c.tag)
                print(c)
                continue
            if "DW_AT_upper_bound" not in c.attributes:
                print("array dimension without upper bound")
                dimensions.append(0)
                continue
            dimensions.append(c.attributes["DW_AT_upper_bound"].value + 1)
        return dimensions

    @staticmethod
    def from_die(die):
        dimensions = DwarfArray.get_dimensions(die)
        if "DW_AT_byte_size" not in die.attributes:
            size = 0
        else:
            size = die.attributes["DW_AT_byte_size"].value
        ref_die = die.get_DIE_from_attribute("DW_AT_type")
        datatype=get_datatype_from_die(ref_die)
        return DwarfArray(
            dimensions=dimensions, size=size, datatype=datatype
        )

@dataclass
class DwarfStructure:
    size: int
    name: str = None
    members: dict[str, DwarfMember] = field(default_factory=dict)

    @staticmethod
    def from_die(die) -> Self:
        size = die.attributes["DW_AT_byte_size"].value
        members = {}
        _self = DwarfStructure(size=size, members=members)
        for child in die.iter_children():
            if child.tag != "DW_TAG_member":
                print("structure child but not member?")
                print(child)
                continue
            m = DwarfMember.from_die(child)
            m.datatype = get_datatype_from_die(
                child.get_DIE_from_attribute("DW_AT_type")
            )
            members[m.name] = m
        return _self


@dataclass
class DwarfEnum:
    name: str = None
    members: dict[str, int] = field(default_factory=dict)

    @staticmethod
    def from_die(die) -> Self:
        members = {}
        for child in die.iter_children():
            if child.tag != "DW_TAG_enumerator":
                print("enum child but not enumerator?")
                print(child)
                continue
            name = child.attributes["DW_AT_name"].value.decode("utf-8")
            value = child.attributes["DW_AT_const_value"].value
            members[name] = value
        return DwarfEnum(members=members)


@dataclass
class DwarfVariable:
    name: str
    location: int
    datatype: Any = None

    @staticmethod
    def from_die(die):
        name = die.attributes["DW_AT_name"].value.decode("utf-8")
        parser = DWARFExprParser(die.cu.structs)
        op = parser.parse_expr(die.attributes["DW_AT_location"].value)
        if len(op) != 1 or op[0].op_name != "DW_OP_addr":
            print("unknown location type", die.attributes["DW_AT_location"].value)
            return None
        ref_die = die.get_DIE_from_attribute("DW_AT_type")
        return DwarfVariable(
            name=name, location=op[0].args[0], datatype=get_datatype_from_die(ref_die)
        )
    
def get_datatype_from_die(die, datatype_name="Unknown"):
    dimensions = [1]

    if die.tag == "DW_TAG_array_type":
        return DwarfArray.from_die(die)

    if die.tag == "DW_TAG_typedef":
        datatype_name = die.attributes["DW_AT_name"].value.decode("utf-8")
        if datatype_name in basetypes:
            return basetypes[datatype_name]
        if not "DW_AT_type" in die.attributes:
            print("typedef without type", die.attributes["DW_AT_name"].value)
            return None
        ref_die = die.get_DIE_from_attribute("DW_AT_type")
        return get_datatype_from_die(ref_die, datatype_name=datatype_name)

    if die.tag == "DW_TAG_structure_type" or die.tag == "DW_TAG_union_type":
        struct = DwarfStructure.from_die(die)
        struct.name = datatype_name
        return struct

    if die.tag == "DW_TAG_enumeration_type":
        enum = DwarfEnum.from_die(die)
        enum.name = datatype_name
        return enum

    if die.tag == "DW_TAG_base_type":
        name = die.attributes["DW_AT_name"].value.decode("utf-8")
        size = die.attributes["DW_AT_byte_size"].value
        return DwarfBaseType(name, size)

    if die.tag == "DW_TAG_subroutine_type":
        return DwarfBaseType("Function", 0)


    if die.tag == "DW_TAG_unspecified_type":
        return DwarfBaseType("void", 0)

    tags_to_follow = [
        "DW_TAG_const_type",
        "DW_TAG_pointer_type",
        "DW_TAG_volatile_type",
    ]

    if die.tag in tags_to_follow:
        return get_datatype_from_die(die.get_DIE_from_attribute("DW_AT_type"))


    print("unknown datatype", die.tag)
    print(die)
    return None