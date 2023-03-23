from dataclasses import fields
from pathlib import Path
from typing import Any, Callable, Tuple
import functools

from ..model.compu_methods import (
    A2LCompuMethodFormula,
    A2LCompuMethodLinear,
    A2LCompuMethodRational,
    A2LCompuMethodTableInterpolation,
    A2LCompuMethodTableNoInterpolation,
    A2LCompuMethodVerbalTable,
)

from .util import (
    Lexer,
    add_key_values,
    is_number,
    parse_list_of_numbers,
    parse_members,
    parse_number,
    parse_string,
    parse_with_lexer,
)
from ..model.model import (
    A2LAnnotation,
    A2LAxisDescription,
    A2LAxisDescriptionComAxis,
    A2LAxisDescriptionCurveAxis,
    A2LAxisDescriptionFixAxis,
    A2LAxisDescriptionResAxis,
    A2LAxisPts,
    A2LBlob,
    A2LCompuMethod,
    A2LCompuTab,
    A2LCompuVTab,
    A2LCompuVTabRange,
    A2LInstance,
    A2LModCommon,
    A2LRecordLayout,
    A2LRecordLayoutAxisPts,
    A2LRecordLayoutNoAxisPts,
    A2LStructure,
    A2LStructureComponent,
    A2LTransformer,
    A2LTypedefAxis,
    A2lFncValues,
    A2lLRescaleAxis,
    ByteOrder,
)
from ..model.characteristic_model import (
    A2LCharacteristic,
    A2LCharacteristicArray,
    A2LCharacteristicCube4,
    A2LCharacteristicCuboid,
    A2LCharacteristicCurve,
    A2LCharacteristicMap,
    A2LCharacteristicTypedef,
    A2LCharacteristicValue,
    A2LCharactersiticAscii,
    A2LMeasurement,
    DependentCharacteristic,
    VirtualCharacteristic,
    VirtualMeasurement,
)

from ..model.project_model import (
    A2LFunction,
    A2LGroup,
    A2LHeader,
    A2LModule,
    A2LProject,
    A2lFile,
)
from ..model.mod_par_model import (
    A2LIfData,
    A2LMemorySegment,
    A2LModPar,
)


def project(tokens: list[str]) -> Tuple[dict, list[str]]:
    if tokens[0] != "PROJECT":
        raise Exception("PROJECT expected, got " + tokens[0] + "")

    params = {}
    lexer: Lexer = {
        "/begin": lambda x: ({}, x[1:]),
        "HEADER": header,
        "MODULE": module,
    }

    params["name"] = tokens[1]
    params["description"], tokens = parse_string(tokens[2:])

    tokens = parse_with_lexer(lexer=lexer, name="PROJECT", tokens=tokens, params=params)
    return (
        {"project": A2LProject(**params)},
        tokens[2:],
    )


def header(tokens: list[str]) -> Tuple[dict, list[str]]:
    if tokens[0] != "HEADER":
        raise Exception("HEADER expected")
    tokens = tokens[1:]
    params = {}
    params["description"], tokens = parse_string(tokens)

    def version(tokens: list[str]) -> Tuple[dict, list[str]]:
        version, tokens = parse_string(tokens)
        return {"version": version}, tokens

    lexer: Lexer = {
        "VERSION": version,
        "PROJECT_NO": lambda x: ({"project_number": x[1]}, x[2:]),
    }
    tokens = parse_with_lexer(lexer=lexer, name="HEADER", tokens=tokens, params=params)
    return {"header": A2LHeader(**params)}, tokens


def group(tokens: list[str]) -> Tuple[dict, list[str]]:
    if tokens[0] != "GROUP":
        raise Exception("GROUP expected, got " + tokens[0])
    tokens = tokens[1:]

    params = {}
    params["name"] = tokens[0]
    params["description"], tokens = parse_string(tokens[1:])

    lexer = {
        "ROOT": lambda x: ({}, x[1:]),
        "/begin": lambda x: ({}, x[1:]),
        "SUB_GROUP": functools.partial(
            parse_members, field="sub_groups", name="SUB_GROUP"
        ),
        "REF_CHARACTERISTIC": functools.partial(
            parse_members, field="characteristics", name="REF_CHARACTERISTIC"
        ),
        "REF_MEASUREMENT": functools.partial(
            parse_members, field="measurements", name="REF_MEASUREMENT"
        ),
        "FUNCTION_LIST": functools.partial(
            parse_members, field="function_lists", name="FUNCTION_LIST"
        ),
    }

    tokens = parse_with_lexer(lexer=lexer, name="GROUP", tokens=tokens, params=params)
    return {"groups": [A2LGroup(**params)]}, tokens


def transformer(tokens: list[str]) -> Tuple[dict, list[str]]:
    if tokens[0] != "TRANSFORMER":
        raise Exception("TRANSFORMER expected, got " + tokens[0])
    tokens = tokens[1:]

    params = {}
    params["name"] = tokens[0]
    params["version"], tokens = parse_string(tokens[1:])
    params["name_32bit_dll"], tokens = parse_string(tokens)
    params["name_64bit_dll"], tokens = parse_string(tokens)
    params["timeout_in_ms"] = parse_number(tokens[0])
    params["event"] = tokens[1]
    params["reverse_transformer"] = tokens[2]
    tokens = tokens[3:]
    lexer = {
        "/begin": lambda x: ({}, x[1:]),
        "TRANSFORMER_IN_OBJECTS": functools.partial(
            parse_members, field="in_objects", name="TRANSFORMER_IN_OBJECTS"
        ),
        "TRANSFORMER_OUT_OBJECTS": functools.partial(
            parse_members, field="out_objects", name="TRANSFORMER_OUT_OBJECTS"
        ),
    }
    tokens = parse_with_lexer(
        lexer=lexer, name="TRANSFORMER", tokens=tokens, params=params
    )
    return {"transformers": [A2LTransformer(**params)]}, tokens


def blob(tokens: list[str]) -> Tuple[dict, list[str]]:
    if tokens[0] != "BLOB":
        raise Exception("BLOB expected, got " + tokens[0])
    tokens = tokens[1:]

    params = {}
    params["name"] = tokens[0]
    params["description"], tokens = parse_string(tokens[1:])
    params["ecu_address"] = parse_number(tokens[0])
    params["number_of_bytes"] = parse_number(tokens[1])
    tokens = tokens[2:]
    lexer = {
        "CALIBRATION_ACCESS": lambda x: ({"calibration_access": x[1]}, x[2:]),
    }
    tokens = parse_with_lexer(lexer=lexer, name="BLOB", tokens=tokens, params=params)
    return {"blobs": [A2LBlob(**params)]}, tokens


def typedef_structure(tokens: list[str]) -> Tuple[dict, list[str]]:
    if tokens[0] != "TYPEDEF_STRUCTURE":
        raise Exception("TYPEDEF_STRUCTURE expected, got " + tokens[0])
    tokens = tokens[1:]

    params = {}
    params["name"] = tokens[0]
    params["description"], tokens = parse_string(tokens[1:])
    params["size"] = parse_number(tokens[0])
    tokens = tokens[1:]

    def structure_component(tokens: list[str]) -> Tuple[dict, list[str]]:
        params = {}
        params["name"] = tokens[0]
        params["datatype"] = tokens[1]
        params["offset"] = parse_number(tokens[2])
        if tokens[3] == "MATRIX_DIM":
            params2, tokens = parse_matrix_dim(tokens[3:])
            params.update(params2)
        else:
            tokens = tokens[3:]
        return {"components": [A2LStructureComponent(**params)]}, tokens[2:]

    lexer = {
        "/begin": lambda x: ({}, x[1:]),
        "STRUCTURE_COMPONENT": lambda x: structure_component(x[1:]),
    }
    tokens = parse_with_lexer(
        lexer=lexer, name="TYPEDEF_STRUCTURE", tokens=tokens, params=params
    )
    return {"typedef_structures": [A2LStructure(**params)]}, tokens


def typedef_axis(tokens: list[str]) -> Tuple[dict, list[str]]:
    if tokens[0] != "TYPEDEF_AXIS":
        raise Exception("TYPEDEF_AXIS expected, got " + tokens[0])
    tokens = tokens[1:]
    params = {}
    params["name"] = tokens[0]
    params["description"], tokens = parse_string(tokens[1:])
    params["measurement"] = tokens[0]
    params["record_layout"] = tokens[1]
    params["max_diff"] = parse_number(tokens[2])
    params["compu_method"] = tokens[3]
    params["max_number_of_axis_points"] = parse_number(tokens[4])
    params["lower_limit"] = parse_number(tokens[5])
    params["upper_limit"] = parse_number(tokens[6])
    tokens = tokens[9:]
    return {"typedef_axes": [A2LTypedefAxis(**params)]}, tokens


def module(tokens: list[str]) -> Tuple[dict, list[str]]:
    if tokens[0] != "MODULE":
        raise Exception("MODULE expected, got " + tokens[0])

    params = {}
    params["name"] = tokens[1]
    params["description"], tokens = parse_string(tokens[2:])

    lexer: Lexer = {
        "/begin": lambda x: ({}, x[1:]),
        "MOD_PAR": mod_par,
        "MOD_COMMON": mod_common,
        "IF_DATA": if_data,
        "COMPU_METHOD": compu_method,
        "COMPU_TAB": compu_tab,
        "COMPU_VTAB": compu_vtab,
        "COMPU_VTAB_RANGE": compu_vtab_range,
        "MEASUREMENT": measurement,
        "RECORD_LAYOUT": record_layout,
        "CHARACTERISTIC": characteristic,
        "FUNCTION": function_type,
        "GROUP": group,
        "TYPEDEF_CHARACTERISTIC": typedef_characteristic,
        "INSTANCE": instance,
        "AXIS_PTS": axis_pts,
        "TYPEDEF_AXIS": typedef_axis,
        "TYPEDEF_STRUCTURE": typedef_structure,
        "TRANSFORMER": transformer,
        "BLOB": blob,
    }

    tokens = parse_with_lexer(lexer=lexer, name="MODULE", tokens=tokens, params=params)
    return {"modules": [A2LModule(**params)]}, tokens


def if_data(tokens: list[str]) -> Tuple[dict, list[str]]:
    if tokens[0] != "IF_DATA":
        raise Exception("IF_DATA expected, got " + tokens[0])
    tokens = tokens[1:]

    params = {}
    params["name"] = tokens[0]
    tokens = tokens[1:]
    params["content"] = []
    while tokens[0] != "/end" or tokens[1] != "IF_DATA":
        params["content"].append(tokens[0])
        tokens = tokens[1:]

    return {"if_data": [A2LIfData(**params)]}, tokens[2:]


def memory_segment(tokens: list[str]) -> Tuple[dict, list[str]]:
    params = {}
    params["name"] = tokens[0]
    params["description"], tokens = parse_string(tokens[1:])
    params["program_type"] = tokens[0]
    params["memory_type"] = tokens[1]
    params["location"] = tokens[2]
    params["address"] = parse_number(tokens[3])
    params["size"] = parse_number(tokens[4])
    params["offsets"], tokens = parse_list_of_numbers(tokens[5:])

    lexer = {"/begin": lambda x: ({}, x[1:]), "IF_DATA": if_data}
    tokens = parse_with_lexer(
        lexer=lexer, name="MEMORY_SEGMENT", tokens=tokens, params=params
    )
    return {"memory_segments": [A2LMemorySegment(**params)]}, tokens


def mod_par(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "MOD_PAR":
        raise Exception("MOD_PAR expected")

    params = {}
    params["description"], tokens = parse_string(tokens[1:])

    def system_constant(tokens: list[str]) -> Tuple[dict, list[str]]:
        name, tokens = parse_string(tokens[1:])
        val, tokens = parse_string(tokens)
        return {"system_constants": {name: val}}, tokens

    lexer = {
        "NO_OF_INTERFACES": lambda x: (
            {"number_of_interfaces": parse_number(x[1])},
            x[2:],
        ),
        "/begin": lambda x: ({}, x[1:]),
        "MEMORY_SEGMENT": memory_segment,
        "SYSTEM_CONSTANT": system_constant,
    }
    tokens = parse_with_lexer(lexer=lexer, name="MOD_PAR", tokens=tokens, params=params)

    return {"mod_par": [A2LModPar(**params)]}, tokens


def mod_common(tokens: list[str]) -> Tuple[dict, list[str]]:
    if tokens[0] != "MOD_COMMON":
        raise Exception("MOD_COMMON expected")
    tokens = tokens[1:]

    params = {}
    params["description"], tokens = parse_string(tokens)
    lexer = {
        "DEPOSIT": lambda x: ({"deposit": x[1]}, x[2:]),
        "BYTE_ORDER": lambda x: ({"byte_order": ByteOrder(x[1])}, x[2:]),
        "ALIGNMENT_BYTE": lambda x: ({"alignment_byte": parse_number(x[1])}, x[2:]),
        "ALIGNMENT_WORD": lambda x: ({"alignment_word": parse_number(x[1])}, x[2:]),
        "ALIGNMENT_LONG": lambda x: ({"alignment_long": parse_number(x[1])}, x[2:]),
        "ALIGNMENT_FLOAT32_IEEE": lambda x: (
            {"alignment_float32_ieee": parse_number(x[1])},
            x[2:],
        ),
        "ALIGNMENT_FLOAT64_IEEE": lambda x: (
            {"alignment_float64_ieee": parse_number(x[1])},
            x[2:],
        ),
    }
    tokens = parse_with_lexer(
        lexer=lexer, name="MOD_COMMON", tokens=tokens, params=params
    )
    return {"mod_common": [A2LModCommon(**params)]}, tokens


def tab_intp(tokens: list[str]) -> Tuple[Any, list[str]]:
    params = {}
    if tokens[0] == "COMPU_TAB_REF":
        params["compu_tab_ref"] = tokens[1]
        tokens = tokens[2:]
    else:
        values = {}
        size = parse_number(tokens[0])
        tokens = tokens[1:]
        for _ in range(size):
            x = parse_number(tokens[0])
            y = parse_number(tokens[1])
            values[x] = y
            tokens = tokens[2:]
        params["values"] = values

    if tokens[0] == "DEFAULT_VALUE_NUMERIC":
        params["default_value"] = parse_number(tokens[1])
        tokens = tokens[2:]

    return params, tokens[2:]


def compu_method(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "COMPU_METHOD":
        raise Exception("COMPU_METHOD expected, got " + tokens[0])

    params = {}
    params["name"] = tokens[1]
    params["description"], tokens = parse_string(tokens[2:])

    compu_method_types = {
        "IDENTICAL": A2LCompuMethod,
        "LINEAR": A2LCompuMethodLinear,
        "RAT_FUNC": A2LCompuMethodRational,
        "FORM": A2LCompuMethodFormula,
        "TAB_INTP": A2LCompuMethodTableInterpolation,
        "TAB_NOINTP": A2LCompuMethodTableNoInterpolation,
        "TAB_VERB": A2LCompuMethodVerbalTable,
    }
    compu_method_type = tokens[0]

    params["format"] = tokens[1]
    params["unit"], tokens = parse_string(tokens[2:])

    def coeffs(tokens: list[str]) -> Tuple[Any, list[str]]:
        coeffs = []
        tokens = tokens[1:]
        while is_number(tokens[0]):
            coeffs.append(parse_number(tokens[0]))
            tokens = tokens[1:]
        return {"coeffs": coeffs}, tokens

    def formula(tokens: list[str]) -> Tuple[Any, list[str]]:
        tokens = tokens[1:]
        formula_inv = None
        formula = None
        while tokens[0] != "/end" or tokens[1] != "FORMULA":
            if tokens[0] == "FORMULA_INV":
                formula_inv, tokens = parse_string(tokens[1:])
            else:
                formula, tokens = parse_string(tokens)
        return {"formula": formula, "formula_inv": formula_inv}, tokens[2:]

    if compu_method_type == "TAB_INTP" or compu_method_type == "TAB_NOINTP":
        params2, tokens = tab_intp(tokens)
        params.update(params2)
    else:
        lexer = {
            "COEFFS_LINEAR": coeffs,
            "COEFFS": coeffs,
            "STATUS_STRING_REF": lambda x: ({"status_string_ref": x[1]}, x[2:]),
            "/begin": lambda x: ({}, x[1:]),
            "FORMULA": formula,
            "COMPU_TAB_REF": lambda x: ({"compu_tab_ref": x[1]}, x[2:]),
        }
        tokens = parse_with_lexer(lexer, "COMPU_METHOD", params, tokens)
    class_ = compu_method_types[compu_method_type]
    return {"compu_methods": [class_(**params)]}, tokens


def compu_tab(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "COMPU_TAB":
        raise Exception("COMPU_TAB expected, got " + tokens[0])

    params = {}
    params["name"] = tokens[1]
    params["description"], tokens = parse_string(tokens[2:])
    params["table_type"] = tokens[0]

    params2, tokens = tab_intp(tokens[1:])
    params.update(params2)

    return {"compu_tabs": [A2LCompuTab(**params)]}, tokens


def compu_vtab(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "COMPU_VTAB":
        raise Exception("COMPU_VTAB expected, got " + tokens[0])

    params = {}
    params["name"] = tokens[1]
    params["description"], tokens = parse_string(tokens[2:])

    if tokens[0] != "TAB_VERB":
        raise Exception("TAB_VERB expected, got " + tokens[0])

    tokens = tokens[1:]
    size = parse_number(tokens[0])
    tokens = tokens[1:]
    values = {}
    for _ in range(size):
        val = parse_number(tokens[0])
        name, tokens = parse_string(tokens[1:])
        values[val] = name
    params["values"] = values

    if tokens[0] == "DEFAULT_VALUE":
        params["default_value"], tokens = parse_string(tokens[1:])

    assert tokens[0] == "/end", "Expected /end, got " + tokens[0]

    return {"compu_vtabs": [A2LCompuVTab(**params)]}, tokens[2:]


def compu_vtab_range(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "COMPU_VTAB_RANGE":
        raise Exception("COMPU_VTAB_RANGE expected, got " + tokens[0])

    params = {}
    params["name"] = tokens[1]
    params["description"], tokens = parse_string(tokens[2:])

    size = parse_number(tokens[0])
    tokens = tokens[1:]
    values = {}
    for _ in range(size):
        min = parse_number(tokens[0])
        max = parse_number(tokens[1])
        name, tokens = parse_string(tokens[2:])
        values[(min, max)] = name
    params["values"] = values

    if tokens[0] == "DEFAULT_VALUE":
        params["default_value"], tokens = parse_string(tokens[1:])

    assert tokens[0] == "/end", "Expected /end, got " + tokens[0]

    return {"compu_vtab_ranges": [A2LCompuVTabRange(**params)]}, tokens[2:]


def parse_matrix_dim(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "MATRIX_DIM":
        raise Exception("MATRIX_DIM expected, got " + tokens[0])

    dimensions = []

    tokens = tokens[1:]
    while is_number(tokens[0]):
        dimensions.append(parse_number(tokens[0]))
        tokens = tokens[1:]

    return {"matrix_dim": dimensions}, tokens


def measurement(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "MEASUREMENT":
        raise Exception("MEASUREMENT expected, got " + tokens[0])

    params = {}
    params["name"] = tokens[1]
    description, tokens = parse_string(tokens[2:])
    params["description"] = description

    params["datatype"] = tokens[0]
    params["compu_method"] = tokens[1]
    # tokens[2] = ?
    # tokens[3] = ?
    params["min"] = parse_number(tokens[4])
    params["max"] = parse_number(tokens[5])

    tokens = tokens[6:]

    def virtual_measurement(tokens: list[str]) -> Tuple[Any, list[str]]:
        tokens = tokens[1:]
        variables = []
        while tokens[0] != "/end" or tokens[1] != "VIRTUAL":
            variables.append(tokens[0])
            tokens = tokens[1:]
        return {"virtual": VirtualMeasurement(variables)}, tokens[2:]

    lexer = {
        "EXTENDED_LIMITS": lambda x: (
            {"extended_min": parse_number(x[1]), "extended_max": parse_number(x[2])},
            x[3:],
        ),
        "FORMAT": lambda x: ({"format": x[1]}, x[2:]),
        "DISPLAY_IDENTIFIER": lambda x: ({"display_identifier": x[1]}, x[2:]),
        "BIT_MASK": lambda x: ({"bitmask": parse_number(x[1])}, x[2:]),
        "PHYS_UNIT": lambda x: ({"phys_unit": x[1]}, x[2:]),
        "ECU_ADDRESS_EXTENSION": lambda x: (
            {"ecu_address_extension": parse_number(x[1])},
            x[2:],
        ),
        "DISCRETE": lambda x: ({"discrete": True}, x[1:]),
        "/begin": lambda x: ({}, x[1:]),
        "MATRIX_DIM": lambda x: parse_matrix_dim(x),
        "ANNOTATION": lambda x: parse_annotation(x),
        "ECU_ADDRESS": lambda x: ({"ecu_address": parse_number(x[1])}, x[2:]),
        "IF_DATA": if_data,
        "VIRTUAL": lambda x: virtual_measurement(x),
    }

    tokens = parse_with_lexer(
        lexer=lexer, name="MEASUREMENT", tokens=tokens, params=params
    )

    return {"measurements": [A2LMeasurement(**params)]}, tokens


def record_layout(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "RECORD_LAYOUT":
        raise Exception("RECORD_LAYOUT expected, got " + tokens[0])

    params = {}
    params["name"] = tokens[2]
    tokens = tokens[2:]

    def fnc_value(tokens: list[str]) -> Tuple[Any, list[str]]:
        params = {}
        params["position"] = parse_number(tokens[1])
        params["datatype"] = tokens[2]
        params["index_mode"] = tokens[3]
        params["addressing_mode"] = tokens[4]
        return {"fields": [A2lFncValues(**params)]}, tokens[5:]

    def axis_value(tokens: list[str]) -> Tuple[Any, list[str]]:
        params = {}
        params["axis"] = tokens[0]
        params["position"] = parse_number(tokens[1])
        params["datatype"] = tokens[2]
        params["index_mode"] = tokens[3]
        params["addressing_mode"] = tokens[4]
        return {"fields": [A2LRecordLayoutAxisPts(**params)]}, tokens[5:]

    def rescale_axis(tokens: list[str]) -> Tuple[Any, list[str]]:
        params = {}
        params["axis"] = tokens[0]
        params["position"] = parse_number(tokens[1])
        params["datatype"] = tokens[2]
        params["map_position"] = parse_number(tokens[3])
        params["index_mode"] = tokens[4]
        params["addressing_mode"] = tokens[5]
        return {"fields": [A2lLRescaleAxis(**params)]}, tokens[6:]

    def no_axis_value(tokens: list[str]) -> Tuple[Any, list[str]]:
        params = {}
        params["axis"] = tokens[0]
        params["position"] = parse_number(tokens[1])
        params["datatype"] = tokens[2]
        return {"fields": [A2LRecordLayoutNoAxisPts(**params)]}, tokens[3:]

    lexer = {
        "FNC_VALUES": fnc_value,
        "AXIS_PTS_X": axis_value,
        "AXIS_PTS_Y": axis_value,
        "AXIS_PTS_Z": axis_value,
        "AXIS_PTS_4": axis_value,
        "AXIS_PTS_5": axis_value,
        "AXIS_RESCALE_X": axis_value,
        "NO_AXIS_PTS_X": no_axis_value,
        "NO_AXIS_PTS_Y": no_axis_value,
        "NO_AXIS_PTS_Z": no_axis_value,
        "NO_AXIS_PTS_4": no_axis_value,
        "NO_AXIS_PTS_5": no_axis_value,
        "NO_RESCALE_X": no_axis_value,
        "RESERVED": no_axis_value,
        "AXIS_RESCALE_X": rescale_axis,
    }

    tokens = parse_with_lexer(
        lexer=lexer, name="RECORD_LAYOUT", tokens=tokens, params=params
    )

    return {"record_layouts": [A2LRecordLayout(**params)]}, tokens


def parse_annotation(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "ANNOTATION":
        raise Exception("ANNOTATION expected, got " + tokens[0])

    tokens = tokens[1:]

    params = {}

    def parse_s(tokens: list[str], field: str) -> Tuple[dict, list[str]]:
        val, tokens = parse_string(tokens)
        return {field: val}, tokens

    def parse_annotation_text(tokens: list[str]) -> Tuple[dict, list[str]]:
        text = None
        while tokens[0] != "/end" or tokens[1] != "ANNOTATION_TEXT":
            text, tokens = parse_string(tokens)
        return {"text": text}, tokens[2:]

    lexer = {
        "ANNOTATION_LABEL": lambda x: functools.partial(parse_s, field="label")(x[1:]),
        "ANNOTATION_ORIGIN": lambda x: functools.partial(parse_s, field="origin")(
            x[1:]
        ),
        "ANNOTATION_TEXT": parse_annotation_text,
        "/begin": lambda x: ({}, x[1:]),
    }

    tokens = parse_with_lexer(
        lexer=lexer, name="ANNOTATION", tokens=tokens, params=params
    )
    return {"annotations": A2LAnnotation(**params)}, tokens


def parse_axis_descr(tokens: list[str]) -> Tuple[dict, list[str]]:
    if tokens[0] != "AXIS_DESCR":
        raise Exception("AXIS_DESCR expected, got " + tokens[0])

    tokens = tokens[1:]

    axis_types = {
        "STD_AXIS": A2LAxisDescription,
        "FIX_AXIS": A2LAxisDescriptionFixAxis,
        "COM_AXIS": A2LAxisDescriptionComAxis,
        "CURVE_AXIS": A2LAxisDescriptionCurveAxis,
        "RES_AXIS": A2LAxisDescriptionResAxis,
    }
    if tokens[0] not in axis_types:
        raise Exception("Unknown axis type " + tokens[0])

    axis_type = axis_types[tokens[0]]
    params = {}
    params["measurement"] = tokens[1]
    params["compu_method"] = tokens[2]
    params["size"] = parse_number(tokens[3])
    params["min"] = parse_number(tokens[4])
    params["max"] = parse_number(tokens[5])

    tokens = tokens[6:]

    def fix_axis_par_dist(tokens: list[str]) -> Tuple[Any, list[str]]:
        numbers, tokens = parse_list_of_numbers(tokens[1:])
        return {"par_dist": numbers}, tokens

    def fix_axis_par_list(tokens: list[str]) -> Tuple[Any, list[str]]:
        numbers, tokens = parse_list_of_numbers(tokens[1:])
        return {"par_list": numbers}, tokens[2:]

    lexer = {
        "AXIS_PTS_REF": lambda x: ({"axis_pts_ref": x[1]}, x[2:]),
        "CURVE_AXIS_REF": lambda x: ({"curve_axis_ref": x[1]}, x[2:]),
        "MONOTONY": lambda x: ({"monotony": x[1]}, x[2:]),
        "/begin": lambda x: ({}, x[1:]),
        "FIX_AXIS_PAR_DIST": fix_axis_par_dist,
        "FIX_AXIS_PAR_LIST": fix_axis_par_list,
    }

    tokens = parse_with_lexer(
        lexer=lexer, name="AXIS_DESCR", tokens=tokens, params=params
    )
    return {"axis_descriptions": [axis_type(**params)]}, tokens


def characteristic(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "CHARACTERISTIC":
        raise Exception("CHARACTERISTIC expected, got " + tokens[0])

    params = {}
    params["name"] = tokens[1]
    params["description"], tokens = parse_string(tokens[2:])

    characteristic_type = tokens[0]

    char_types = {
        "VALUE": (A2LCharacteristicValue, []),
        "VAL_BLK": (A2LCharacteristicArray, ["MATRIX_DIM"]),
        "ASCII": (A2LCharactersiticAscii, ["NUMBER"]),
        "CURVE": (A2LCharacteristicCurve, ["AXIS_DESCR"]),
        "MAP": (A2LCharacteristicMap, ["AXIS_DESCR"]),
        "CUBOID": (A2LCharacteristicCuboid, ["AXIS_DESCR"]),
        "CUBE_4": (A2LCharacteristicCube4, ["AXIS_DESCR"]),
    }

    if not characteristic_type in char_types:
        raise Exception("Unknown characteristic type, got " + tokens[0])

    char_type, expected_keywords = char_types[characteristic_type]

    params["ecu_address"] = parse_number(tokens[1])
    params["record_layout"] = tokens[2]
    params["maxdiff"] = parse_number(tokens[3])
    params["compu_method"] = tokens[4]
    params["min"] = parse_number(tokens[5])
    params["max"] = parse_number(tokens[6])

    tokens = tokens[7:]

    def dependent_characteristic(tokens: list[str]) -> Tuple[Any, list[str]]:
        tokens = tokens[1:]
        formula, tokens = parse_string(tokens)
        variables = []
        while tokens[0] != "/end" or tokens[1] != "DEPENDENT_CHARACTERISTIC":
            variables.append(tokens[0])
            tokens = tokens[1:]
        return {
            "dependent_characteristic": DependentCharacteristic(formula, variables)
        }, tokens[2:]

    def virtual_characteristic(tokens: list[str]) -> Tuple[Any, list[str]]:
        tokens = tokens[1:]
        formula, tokens = parse_string(tokens)
        variables = []
        while tokens[0] != "/end" or tokens[1] != "VIRTUAL_CHARACTERISTIC":
            variables.append(tokens[0])
            tokens = tokens[1:]
        return {
            "virtual_characteristic": VirtualCharacteristic(formula, variables)
        }, tokens[2:]

    lexer = {
        "EXTENDED_LIMITS": lambda x: (
            {"extended_min": parse_number(x[1]), "extended_max": parse_number(x[2])},
            x[3:],
        ),
        "FORMAT": lambda x: ({"format": x[1]}, x[2:]),
        "DISPLAY_IDENTIFIER": lambda x: ({"display_identifier": x[1]}, x[2:]),
        "BIT_MASK": lambda x: ({"bitmask": parse_number(x[1])}, x[2:]),
        "NUMBER": lambda x: ({"size": parse_number(x[1])}, x[2:]),
        "PHYS_UNIT": lambda x: ({"phys_unit": x[1]}, x[2:]),
        "ECU_ADDRESS_EXTENSION": lambda x: (
            {"ecu_address_extension": parse_number(x[1])},
            x[2:],
        ),
        "DISCRETE": lambda x: ({"discrete": True}, x[1:]),
        "/begin": lambda x: ({}, x[1:]),
        "MATRIX_DIM": lambda x: parse_matrix_dim(x),
        "AXIS_DESCR": lambda x: parse_axis_descr(x),
        "ANNOTATION": lambda x: parse_annotation(x),
        "DEPENDENT_CHARACTERISTIC": lambda x: dependent_characteristic(x),
        "VIRTUAL_CHARACTERISTIC": lambda x: virtual_characteristic(x),
        "MODEL_LINK": lambda x: ({"model_link": x[1]}, x[2:]),
    }

    tokens = parse_with_lexer(
        lexer=lexer, name="CHARACTERISTIC", tokens=tokens, params=params
    )

    field_names = [field.name for field in fields(char_type)]
    char_type_params = {k: v for k, v in params.items() if k in field_names}
    params = {k: v for k, v in params.items() if k not in field_names}
    params["typedef"] = char_type(**char_type_params)

    return {"characteristics": [A2LCharacteristic(**params)]}, tokens


def typedef_characteristic(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "TYPEDEF_CHARACTERISTIC":
        raise Exception("TYPEDEF_CHARACTERISTIC expected, got " + tokens[0])

    tokens = tokens[1:]

    params = {}
    params["name"] = tokens[0]
    params["description"], tokens = parse_string(tokens[1:])

    characteristic_type = tokens[0]

    char_types = {
        "VALUE": (A2LCharacteristicValue, []),
        "VAL_BLK": (A2LCharacteristicArray, ["MATRIX_DIM"]),
        "ASCII": (A2LCharactersiticAscii, ["NUMBER"]),
        "CURVE": (A2LCharacteristicCurve, ["AXIS_DESCR"]),
        "MAP": (A2LCharacteristicMap, ["AXIS_DESCR"]),
        "CUBOID": (A2LCharacteristicCuboid, ["AXIS_DESCR"]),
        "CUBE_4": (A2LCharacteristicCube4, ["AXIS_DESCR"]),
    }

    if not characteristic_type in char_types:
        raise Exception("Unknown characteristic type, got " + tokens[0])

    char_type, expected_keywords = char_types[characteristic_type]

    params["record_layout"] = tokens[1]
    params["maxdiff"] = parse_number(tokens[2])
    params["compu_method"] = tokens[3]
    params["min"] = parse_number(tokens[4])
    params["max"] = parse_number(tokens[5])

    tokens = tokens[6:]

    lexer = {
        "EXTENDED_LIMITS": lambda x: (
            {"extended_min": parse_number(x[1]), "extended_max": parse_number(x[2])},
            x[3:],
        ),
        "FORMAT": lambda x: ({"format": x[1]}, x[2:]),
        "DISPLAY_IDENTIFIER": lambda x: ({"display_identifier": x[1]}, x[2:]),
        "BIT_MASK": lambda x: ({"bitmask": parse_number(x[1])}, x[2:]),
        "NUMBER": lambda x: ({"size": parse_number(x[1])}, x[2:]),
        "PHYS_UNIT": lambda x: ({"phys_unit": x[1]}, x[2:]),
        "DISCRETE": lambda x: ({"discrete": True}, x[1:]),
        "/begin": lambda x: ({}, x[1:]),
        "MATRIX_DIM": lambda x: parse_matrix_dim(x),
        "AXIS_DESCR": lambda x: parse_axis_descr(x),
        "ANNOTATION": lambda x: parse_annotation(x),
    }

    tokens = parse_with_lexer(
        lexer=lexer, name="TYPEDEF_CHARACTERISTIC", tokens=tokens, params=params
    )

    field_names = [field.name for field in fields(char_type)]
    char_type_params = {k: v for k, v in params.items() if k in field_names}
    params = {k: v for k, v in params.items() if k not in field_names}
    params["typedef"] = char_type(**char_type_params)

    return {"characteristics": [A2LCharacteristicTypedef(**params)]}, tokens


def instance(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "INSTANCE":
        raise Exception("INSTANCE expected, got " + tokens[0])
    tokens = tokens[1:]

    params = {}
    params["name"] = tokens[0]
    params["description"], tokens = parse_string(tokens[1:])
    params["reference"] = tokens[0]
    params["ecu_address"] = parse_number(tokens[1])
    lexer = {
        "MATRIX_DIM": parse_matrix_dim,
        "DISPLAY_IDENTIFIER": lambda x: ({"display_identifier": x[1]}, x[2:]),
    }
    tokens = parse_with_lexer(
        lexer=lexer, name="INSTANCE", tokens=tokens[2:], params=params
    )

    return {"instances": [A2LInstance(**params)]}, tokens


def skip_type(tokens: list[str], name: str) -> Tuple[Any, list[str]]:
    if tokens[0] != name:
        raise Exception(f"{name} expected, got " + tokens[0])

    tokens = tokens[1:]

    while tokens[0] != "/end" or tokens[1] != name:
        tokens = tokens[1:]

    return {}, tokens[2:]


def axis_pts(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "AXIS_PTS":
        raise Exception("AXIS_PTS expected, got " + tokens[0])

    tokens = tokens[1:]
    params = {}
    params["name"] = tokens[0]
    params["description"], tokens = parse_string(tokens[1:])
    params["ecu_address"] = parse_number(tokens[0])
    params["measurement"] = tokens[1]
    params["record_layout"] = tokens[2]
    params["offset"] = parse_number(tokens[3])
    params["compu_method"] = tokens[4]
    params["max_number_sample_points"] = parse_number(tokens[5])
    params["min"] = parse_number(tokens[6])
    params["max"] = parse_number(tokens[7])
    tokens = tokens[8:]

    lexer = {
        "DISPLAY_IDENTIFIER": lambda x: ({"display_identifier": x[1]}, x[2:]),
    }
    tokens = parse_with_lexer(
        lexer=lexer, name="AXIS_PTS", tokens=tokens, params=params
    )
    return {"axis_pts": [A2LAxisPts(**params)]}, tokens


def function_type(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "FUNCTION":
        raise Exception("FUNCTION expected, got " + tokens[0])
    tokens = tokens[1:]

    params = {}
    params["name"] = tokens[0]
    params["description"], tokens = parse_string(tokens[1:])

    lexer = {
        "/begin": lambda x: ({}, x[1:]),
        "SUB_FUNCTION": functools.partial(
            parse_members, field="sub_functions", name="SUB_FUNCTION"
        ),
        "REF_CHARACTERISTIC": functools.partial(
            parse_members, field="ref_characteristics", name="REF_CHARACTERISTIC"
        ),
        "DEF_CHARACTERISTIC": functools.partial(
            parse_members, field="def_characteristics", name="DEF_CHARACTERISTIC"
        ),
        "IN_MEASUREMENT": functools.partial(
            parse_members, field="in_measurements", name="IN_MEASUREMENT"
        ),
        "OUT_MEASUREMENT": functools.partial(
            parse_members, field="out_measurements", name="OUT_MEASUREMENT"
        ),
        "LOC_MEASUREMENT": functools.partial(
            parse_members, field="loc_measurements", name="LOC_MEASUREMENT"
        ),
    }

    tokens = parse_with_lexer(
        lexer=lexer, name="FUNCTION", tokens=tokens, params=params
    )
    return {"functions": [A2LFunction(**params)]}, tokens


def file_to_tokens(path: Path) -> list[str]:
    tokens = []

    with path.open("r", encoding="utf-8-sig") as f:
        lines = f.readlines()
    for line in lines:
        temp = line.strip().split("//")[0].split(" ")
        tokens += temp

    empty_tokens = ["", " ", "\t", "\n"]

    return [t for t in tokens if t not in empty_tokens]


def clean_comments(tokens: list[str]) -> list[str]:
    while "/*" in tokens:
        start = tokens.index("/*")
        end = tokens.index("*/")
        tokens = tokens[:start] + tokens[end + 1 :]

    return tokens


def assp2_version(tokens: list[str]) -> Tuple[dict, list[str]]:
    if tokens[0] != "ASAP2_VERSION":
        raise Exception("ASAP2_VERSION expected")

    major = tokens[1]
    minor = tokens[2]

    return {"asap2_version": f"{major}.{minor}"}, tokens[3:]


def read_a2l(path: Path) -> A2lFile:
    tokens = file_to_tokens(path)

    tokens = clean_comments(tokens)

    lexer = {
        "ASAP2_VERSION": assp2_version,
        "/begin": lambda x: ({}, x[1:]),
        "PROJECT": project,
    }

    params = {}
    while len(tokens) != 0:
        func = lexer.get(tokens[0], None)
        if func is None:
            print(tokens[:20])
            raise Exception(f"Unknown token {tokens[0]}")
        key_value, tokens = func(tokens)
        add_key_values(key_value, params)

    return A2lFile(**params)
