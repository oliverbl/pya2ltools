from pathlib import Path
from typing import Any, Callable, Tuple
import functools

from .util import is_number, parse_int
from .model import (
    A2LAnnotation,
    A2LAxisDescription,
    A2LAxisDescriptionComAxis,
    A2LAxisDescriptionCurveAxis,
    A2LAxisDescriptionFixAxis,
    A2LAxisDescriptionResAxis,
    A2LCompuMethod,
    A2LCompuTab,
    A2LCompuVTab,
    A2LCompuVTabRange,
    A2LModPar,
    A2LRecordLayout,
)
from .characteristic_model import (
    A2LCharacteristic,
    A2LCharacteristicArray,
    A2LCharacteristicCube4,
    A2LCharacteristicCuboid,
    A2LCharacteristicCurve,
    A2LCharacteristicMap,
    A2LCharacteristicValue,
    A2LCharactersiticAscii,
    A2LMeasurement,
    DependentCharacteristic,
    VirtualCharacteristic,
    VirtualMeasurement,
)

from .project_model import A2LHeader, A2LModule, A2LProject, A2lFile


# a lexing function takes a list of tokens and returns and Object and sublist of the tokens, after processing
Lex_function = Callable[[list[str]], Tuple[Any, list[str]]]


def assp2_version(tokens: list[str]) -> Tuple[str, list[str]]:
    if tokens[0] != "ASAP2_VERSION":
        raise Exception("ASAP2_VERSION expected")

    major = tokens[1]
    minor = tokens[2]

    return f"{major}.{minor}", tokens[3:]


def project(tokens: list[str]) -> A2LProject:
    if tokens[0] != "PROJECT":
        raise Exception("PROJECT expected, got " + tokens[0] + "")

    project_name = tokens[1]
    description, tokens = parse_description(tokens[2:])

    modules = []
    _header = None

    while tokens[0] != "/end" or tokens[1] != "PROJECT":
        next = lexer.get(tokens[0], None)
        if next is None:
            raise Exception(f"Unknown token {tokens[0]} when parsing in project")

        obj, tokens = next(tokens)

        if isinstance(obj, A2LModule):
            modules.append(obj)
        elif isinstance(obj, A2LHeader):
            _header = obj
        else:
            raise Exception(f"Unknown object {obj} when parsing in project")

    return (
        A2LProject(
            name=project_name, description=description, modules=modules, header=_header
        ),
        tokens[2:],
    )


def header(tokens: list[str]) -> list[str]:
    if tokens[0] != "HEADER":
        raise Exception("HEADER expected")

    # ignore header for now, skip until / end
    while tokens[0] != "/end" or tokens[1] != "HEADER":
        tokens = tokens[1:]

    return A2LHeader(), tokens[2:]


def module(tokens: list[str]) -> list[str]:
    if tokens[0] != "MODULE":
        raise Exception("MODULE expected, got " + tokens[0])

    module_name = tokens[1]
    description, tokens = parse_description(tokens[2:])

    module = A2LModule(name=module_name, description=description)

    while tokens[0] != "/end" or tokens[1] != "MODULE":
        next = lexer.get(tokens[0], None)
        if next is None:
            raise Exception(f"Unknown token {tokens[0]} when parsing in module")

        obj, tokens = next(tokens)

        if isinstance(obj, A2LModPar):
            module.mod_par.append(obj)
        elif isinstance(obj, A2LCharacteristic):
            module.characteristics.append(obj)
        elif isinstance(obj, A2LCompuMethod):
            module.compu_methods.append(obj)
        elif isinstance(obj, A2LCompuTab):
            module.compu_tabs.append(obj)
        elif isinstance(obj, A2LMeasurement):
            module.measurements.append(obj)

    return module, tokens[2:]


def begin(tokens: list[str]) -> list[str]:
    func = lexer.get(tokens[1], None)
    if func is None:
        print(tokens[:20])
        raise Exception(f"Unknown token {tokens[1]} when parsing /begin")

    return func(tokens[1:])


def mod_par(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "MOD_PAR":
        raise Exception("MOD_PAR expected")

    while tokens[0] != "/end" or tokens[1] != "MOD_PAR":
        tokens = tokens[1:]

    return A2LModPar(), tokens[2:]


def parse_description(tokens: list[str]) -> Tuple[str, list[str]]:
    if tokens[0] == '""':
        return "", tokens[1:]

    description = tokens[0][1:] + " "
    tokens = tokens[1:]

    while not tokens[0].endswith('"'):
        description += tokens[0] + " "
        tokens = tokens[1:]

    description += tokens[0][:-1]

    return description, tokens[1:]


def compu_method(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "COMPU_METHOD":
        raise Exception("COMPU_METHOD expected, got " + tokens[0])

    name = tokens[1]
    description, tokens = parse_description(tokens[2:])

    compu_method = A2LCompuMethod(name=name, description=description)

    while tokens[0] != "/end" or tokens[1] != "COMPU_METHOD":
        tokens = tokens[1:]

    return compu_method, tokens[2:]


def compu_tab(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "COMPU_TAB":
        raise Exception("COMPU_TAB expected, got " + tokens[0])

    name = tokens[1]
    description, tokens = parse_description(tokens[2:])

    compu_tab = A2LCompuTab(name=name, description=description)

    while tokens[0] != "/end" or tokens[1] != "COMPU_TAB":
        tokens = tokens[1:]

    return compu_tab, tokens[2:]


def compu_vtab(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "COMPU_VTAB":
        raise Exception("COMPU_VTAB expected, got " + tokens[0])

    name = tokens[1]
    description, tokens = parse_description(tokens[2:])

    compu_vtab = A2LCompuVTab(name=name, description=description)

    while tokens[0] != "/end" or tokens[1] != "COMPU_VTAB":
        tokens = tokens[1:]

    return compu_vtab, tokens[2:]


def compu_vtab_range(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "COMPU_VTAB_RANGE":
        raise Exception("COMPU_VTAB_RANGE expected, got " + tokens[0])

    name = tokens[1]
    description, tokens = parse_description(tokens[2:])

    compu_vtab_range = A2LCompuVTabRange(name=name, description=description)

    while tokens[0] != "/end" or tokens[1] != "COMPU_VTAB_RANGE":
        tokens = tokens[1:]

    return compu_vtab_range, tokens[2:]


def parse_matrix_dim(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "MATRIX_DIM":
        raise Exception("MATRIX_DIM expected, got " + tokens[0])

    dimensions = []

    tokens = tokens[1:]
    while is_number(tokens[0]):
        dimensions.append(parse_int(tokens[0]))
        tokens = tokens[1:]

    return {"matrix_dim": dimensions}, tokens

def parse_if_data(tokens: list[str]) -> Tuple[Any, list[str]]:
    
    obj, tokens = skip_type(tokens, "IF_DATA")
    return {}, tokens


def measurement(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "MEASUREMENT":
        raise Exception("MEASUREMENT expected, got " + tokens[0])

    
    params = {}
    params["name"] = tokens[1]
    description, tokens = parse_description(tokens[2:])
    params["description"] = description
    
    params["datatype"] = tokens[0]
    params["compu_method"] = tokens[1]
    # tokens[2] = ?
    # tokens[3] = ?
    params["min"] = parse_int(tokens[4])
    params["max"] = parse_int(tokens[5])

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
            {"extended_min": parse_int(x[1]), "extended_max": parse_int(x[2])},
            x[3:],
        ),
        "FORMAT": lambda x: ({"format": x[1]}, x[2:]),
        "DISPLAY_IDENTIFIER": lambda x: ({"display_identifier": x[1]}, x[2:]),
        "BIT_MASK": lambda x: ({"bitmask": parse_int(x[1])}, x[2:]),
        "PHYS_UNIT": lambda x: ({"phys_unit": x[1]}, x[2:]),
        "ECU_ADDRESS_EXTENSION": lambda x: ({"ecu_address_extension": parse_int(x[1])}, x[2:]),
        "DISCRETE": lambda x: ({"discrete": True}, x[1:]),
        "/begin": lambda x: ({}, x[1:]),
        "MATRIX_DIM": lambda x: parse_matrix_dim(x),
        "ANNOTATION": lambda x: parse_annotation(x),
        "ECU_ADDRESS": lambda x: ({"ecu_address": parse_int(x[1])}, x[2:]),
        "IF_DATA": lambda x: parse_if_data(x),
        "VIRTUAL": lambda x: virtual_measurement(x),
    }

    while tokens[0] != "/end" or tokens[1] != "MEASUREMENT":
        func = lexer.get(tokens[0], None)
        if func is None:
            print(tokens[:20])
            raise Exception(
                "Unknown token " + tokens[0] + " when parsing MEASUREMENT"
            )
        key_value, tokens = func(tokens)
        print(key_value)
        print(tokens[:10])
        for k, v in key_value.items():
            if isinstance(v, list):
                if k not in params:
                    params[k] = []
                params[k] += v
            else:
                params[k] = v

    measurement = A2LMeasurement(**params)
    return measurement, tokens[2:]


def record_layout(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "RECORD_LAYOUT":
        raise Exception("RECORD_LAYOUT expected, got " + tokens[0])

    name = tokens[1]
    tokens = tokens[1:]
    while tokens[0] != "/end" or tokens[1] != "RECORD_LAYOUT":
        tokens = tokens[1:]

    return A2LRecordLayout(name=name), tokens[2:]


def parse_annotation(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "ANNOTATION":
        raise Exception("ANNOTATION expected, got " + tokens[0])

    tokens = tokens[1:]

    params = {}

    while tokens[0] != "/end" or tokens[1] != "ANNOTATION":
        if tokens[0] == "ANNOTATION_LABEL":
            params["label"], tokens = parse_description(tokens[1:])
        elif tokens[0] == "ANNOTATION_ORIGIN":
            params["origin"], tokens = parse_description(tokens[1:])
        elif tokens[0] == "/begin" and tokens[1] == "ANNOTATION_TEXT":
            params["text"] = []
            tokens = tokens[2:]
            while tokens[0] != "/end" or tokens[1] != "ANNOTATION_TEXT":
                text, tokens = parse_description(tokens)
                params["text"] = text
            tokens = tokens[2:]
        else:
            print(tokens[:20])
            raise Exception("Unknown token " + tokens[0] + " when parsing ANNOTATION")
    return {"annotations": A2LAnnotation(**params)}, tokens[2:]	


def parse_axis_descr(tokens: list[str]) -> Tuple[A2LAxisDescription, list[str]]:
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
    params["size"] = parse_int(tokens[3])
    params["min"] = parse_int(tokens[4])
    params["max"] = parse_int(tokens[5])

    tokens = tokens[6:]

    def fix_axis_par_dist(tokens: list[str]) -> Tuple[Any, list[str]]:
        numbers = []
        tokens = tokens[1:]
        while is_number(tokens[0]):
            numbers.append(int(tokens[0]))
            tokens = tokens[1:]
        return {"par_dist": numbers}, tokens

    def fix_axis_par_list(tokens: list[str]) -> Tuple[Any, list[str]]:
        numbers = []
        tokens = tokens[1:]
        while is_number(tokens[0]):
            numbers.append(int(tokens[0]))
            tokens = tokens[1:]
        return {"par_dist": numbers}, tokens[2:]

    lexer = {
        "AXIS_PTS_REF": lambda x: ({"axis_pts_ref": x[1]}, x[2:]),
        "CURVE_AXIS_REF": lambda x: ({"curve_axis_ref": x[1]}, x[2:]),
        "MONOTONY": lambda x: ({"monotony": x[1]}, x[2:]),
        "/begin": lambda x: ({}, x[1:]),
        "FIX_AXIS_PAR_DIST": fix_axis_par_dist,
        "FIX_AXIS_PAR_LIST": fix_axis_par_list,
    }

    while tokens[0] != "/end" or tokens[1] != "AXIS_DESCR":
        func = lexer.get(tokens[0], None)
        if func is None:
            print(tokens[:20])
            raise Exception("Unknown token " + tokens[0] + " when parsing AXIS_DESCR")
        key_value, tokens = func(tokens)
        for k, v in key_value.items():
            params[k] = v

    return {"axis_descriptions": [axis_type(**params)]}, tokens[2:]


def characteristic(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "CHARACTERISTIC":
        raise Exception("CHARACTERISTIC expected, got " + tokens[0])

    name = tokens[1]
    description, tokens = parse_description(tokens[2:])

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

    params = {}
    params["ecu_address"] = tokens[1]
    params["record_layout"] = tokens[2]
    params["unknown"] = tokens[3]
    params["compu_method"] = tokens[4]
    params["min"] = tokens[5]
    params["max"] = tokens[6]

    tokens = tokens[7:]

    def dependent_characteristic(tokens: list[str]) -> Tuple[Any, list[str]]:
        tokens = tokens[1:]
        formula, tokens = parse_description(tokens)
        variables = []
        while tokens[0] != "/end" or tokens[1] != "DEPENDENT_CHARACTERISTIC":
            variables.append(tokens[0])
            tokens = tokens[1:]
        return {
            "dependent_characteristic": DependentCharacteristic(formula, variables)
        }, tokens[2:]

    def virtual_characteristic(tokens: list[str]) -> Tuple[Any, list[str]]:
        tokens = tokens[1:]
        formula, tokens = parse_description(tokens)
        variables = []
        while tokens[0] != "/end" or tokens[1] != "VIRTUAL_CHARACTERISTIC":
            variables.append(tokens[0])
            tokens = tokens[1:]
        return {"virtual_characteristic": VirtualCharacteristic(formula, variables)}, tokens[2:]

    lexer = {
        "EXTENDED_LIMITS": lambda x: (
            {"extended_min": parse_int(x[1]), "extended_max": parse_int(x[2])},
            x[3:],
        ),
        "FORMAT": lambda x: ({"format": x[1]}, x[2:]),
        "DISPLAY_IDENTIFIER": lambda x: ({"display_identifier": x[1]}, x[2:]),
        "BIT_MASK": lambda x: ({"bitmask": parse_int(x[1])}, x[2:]),
        "NUMBER": lambda x: ({"size": parse_int(x[1])}, x[2:]),
        "PHYS_UNIT": lambda x: ({"phys_unit": x[1]}, x[2:]),
        "ECU_ADDRESS_EXTENSION": lambda x: ({"ecu_address_extension": parse_int(x[1])}, x[2:]),
        "DISCRETE": lambda x: ({"discrete": True}, x[1:]),
        "/begin": lambda x: ({}, x[1:]),
        "MATRIX_DIM": lambda x: parse_matrix_dim(x),
        "AXIS_DESCR": lambda x: parse_axis_descr(x),
        "ANNOTATION": lambda x: parse_annotation(x),
        "DEPENDENT_CHARACTERISTIC": lambda x: dependent_characteristic(x),
        "VIRTUAL_CHARACTERISTIC": lambda x: virtual_characteristic(x),
        "MODEL_LINK": lambda x: ({"model_link": x[1]}, x[2:]),
    }

    while tokens[0] != "/end" or tokens[1] != "CHARACTERISTIC":
        func = lexer.get(tokens[0], None)
        if func is None:
            print(tokens[:20])
            raise Exception(
                "Unknown token " + tokens[0] + " when parsing CHARACTERISTIC"
            )
        key_value, tokens = func(tokens)
        for k, v in key_value.items():
            if isinstance(v, list):
                if k not in params:
                    params[k] = []
                params[k] += v
            else:
                params[k] = v

    return char_type(name=name, description=description, **params), tokens[2:]


def skip_type(tokens: list[str], name: str) -> Tuple[Any, list[str]]:
    if tokens[0] != name:
        raise Exception(f"{name} expected, got " + tokens[0])

    tokens = tokens[1:]

    while tokens[0] != "/end" or tokens[1] != name:
        tokens = tokens[1:]

    return None, tokens[2:]


def axis_pts(tokens: list[str]) -> Tuple[Any, list[str]]:
    return skip_type(tokens, "AXIS_PTS")


def function_type(tokens: list[str]) -> Tuple[Any, list[str]]:
    return skip_type(tokens, "FUNCTION")


lexer: dict[str, Lex_function] = {
    "ASAP2_VERSION": assp2_version,
    "/begin": begin,
    "PROJECT": project,
    "HEADER": header,
    "MODULE": module,
    "MOD_PAR": mod_par,
    "COMPU_METHOD": compu_method,
    "COMPU_TAB": compu_tab,
    "COMPU_VTAB": compu_vtab,
    "COMPU_VTAB_RANGE": compu_vtab_range,
    "MEASUREMENT": measurement,
    "RECORD_LAYOUT": record_layout,
    "CHARACTERISTIC": characteristic,
    "AXIS_PTS": functools.partial(skip_type, name="AXIS_PTS"),
    "FUNCTION": functools.partial(skip_type, name="FUNCTION"),
    "GROUP": functools.partial(skip_type, name="GROUP"),
    "TYPEDEF_CHARACTERISTIC": functools.partial(
        skip_type, name="TYPEDEF_CHARACTERISTIC"
    ),
    "INSTANCE": functools.partial(skip_type, name="INSTANCE"),
    "TYPEDEF_AXIS": functools.partial(skip_type, name="TYPEDEF_AXIS"),
    "TYPEDEF_STRUCTURE": functools.partial(skip_type, name="TYPEDEF_STRUCTURE"),
    "TRANSFORMER": functools.partial(skip_type, name="TRANSFORMER"),
    "BLOB": functools.partial(skip_type, name="BLOB"),
}


def file_to_tokens(path: Path) -> list[str]:
    tokens = []

    with path.open("r", encoding="utf-8-sig") as f:
        lines = f.readlines()
    for line in lines:
        temp = line.strip().split(" ")
        tokens += temp

    empty_tokens = ["", " ", "\t", "\n"]

    return [t for t in tokens if t not in empty_tokens]


def clean_comments(tokens: list[str]) -> list[str]:
    while "/*" in tokens:
        start = tokens.index("/*")
        end = tokens.index("*/")
        tokens = tokens[:start] + tokens[end + 1 :]

    return tokens


def read_a2l(path: Path) -> A2lFile:
    tokens = file_to_tokens(path)

    tokens = clean_comments(tokens)

    project = None
    asap2_version = None

    while len(tokens) != 0:
        func = lexer.get(tokens[0], None)
        if func is None:
            print(tokens[:20])
            raise Exception(f"Unknown token {tokens[0]}")
        obj, tokens = func(tokens)

        if isinstance(obj, A2LProject):
            project = obj
        elif isinstance(obj, str):
            asap2_version = obj
        else:
            raise Exception("Unknown object type")

    return A2lFile(project=project, asap2_version=asap2_version)
