import re
from typing import Any, Self

from elftools.elf.elffile import ELFFile

from dataclasses import dataclass, field
from .model import DwarfVariable


def str_to_variable_path(var: str) -> list[str | int]:
    path: list[str | int] = []
    # split variable_path by . and [] and return list of strings and indexes between []
    # e.g. "a.b[0].c" -> ["a", "b", 0, "c"]
    for part in re.split(r"(\[|\]|\.)", var):
        if part == ".":
            continue
        if part == "[":
            continue
        if part == "]":
            continue
        if part == "":
            continue
        if part.isdigit():
            path.append(int(part))
        else:
            path.append(part)
    return path


@dataclass
class DwarfInfo:
    variables: dict[str, list[DwarfVariable]] = field(default_factory=dict)
    # CU to datatype cache
    __cache: dict[Any, Any] = field(default_factory=dict)

    @staticmethod
    def from_elffile(file, variable_name: str | None = None) -> Self:
        _self = DwarfInfo()

        with open(file, "rb") as f:
            elffile = ELFFile(f)

            if not elffile.has_dwarf_info():
                print("  file has no DWARF info")
                return
            dwarfinfo = elffile.get_dwarf_info()

            for CU in dwarfinfo.iter_CUs():
                top_DIE = CU.get_top_DIE()
                _self.read_global_variable_info_from_die(
                    top_DIE, variable_name=variable_name
                )
            return _self

    def get_address_by_variable_path(self, variable_path: str) -> int:
        path = str_to_variable_path(variable_path)
        var = self.variables[path[0]][0]
        address = var.location
        for part in path[1:]:
            if isinstance(part, int):
                address += part * var.datatype.datatype.size
                var = var.datatype
            else:
                address += var.datatype.members[part].offset
                var = var.datatype.members[part]
        return address

    def read_global_variable_info_from_die(self, die, variable_name: str = None):
        tags_to_skip = ["DW_TAG_subprogram", "DW_TAG_user"]

        if die.tag in tags_to_skip:
            return

        if die.tag == "DW_TAG_variable":
            if "DW_AT_location" not in die.attributes:
                return

            # for debugging purposes
            if variable_name is not None:
                if die.attributes["DW_AT_name"].value.decode("utf-8") != variable_name:
                    return

            v = DwarfVariable.from_die(die, self.__cache)
            if v.name not in self.variables:
                self.variables[v.name] = []
            self.variables[v.name].append(v)

        for child in die.iter_children():
            self.read_global_variable_info_from_die(child, variable_name)
