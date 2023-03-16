from pathlib import Path
from typing import Any, Callable, Tuple
import functools
from .model import (
    A2LCharacteristic,
    A2LCompuMethod,
    A2LCompuTab,
    A2LCompuVTab,
    A2LCompuVTabRange,
    A2LHeader,
    A2LMeasurement,
    A2LModPar,
    A2LModule,
    A2LProject,
    A2LRecordLayout,
    A2lFile,
)


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

    description = tokens[0][1:]

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

    def is_number(s: str) -> bool:
        try:
            int(s)
            return True
        except ValueError:
            return False

    dimensions = []

    tokens = tokens[1:]
    while is_number(tokens[0]):
        dimensions.append(int(tokens[0]))
        tokens = tokens[1:]

    return dimensions, tokens


def measurement(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "MEASUREMENT":
        raise Exception("MEASUREMENT expected, got " + tokens[0])

    name = tokens[1]
    description, tokens = parse_description(tokens[2:])
    measurement = A2LMeasurement(name=name, description=description)
    datatype = tokens[0]
    symbol_name = tokens[1]
    # tokens[2] = ?
    # tokens[3] = ?
    min = tokens[4]
    max = tokens[5]

    tokens = tokens[6:]

    while tokens[0] != "/end" or tokens[1] != "MEASUREMENT":
        if tokens[0] == "ECU_ADDRESS":
            ecu_address = tokens[1]
            tokens = tokens[2:]
        elif tokens[0] == "FORMAT":
            format = tokens[1]
            tokens = tokens[2:]
        elif tokens[0] == "DISPLAY_IDENTIFIER":
            display_name = tokens[1]
            tokens = tokens[2:]
        elif tokens[0] == "BIT_MASK":
            bitmask = tokens[1]
            tokens = tokens[2:]
        elif tokens[0] == "/begin":
            sub = tokens[1]
            tokens = tokens[2:]
            while tokens[0] != "/end" or tokens[1] != sub:
                tokens = tokens[1:]
            tokens = tokens[2:]
        elif tokens[0] == "MATRIX_DIM":
            matrix_dim, tokens = parse_matrix_dim(tokens)
        elif tokens[0] == "DISCRETE":
            tokens = tokens[1:]
        else:
            print(tokens[:20])
            raise Exception("Unknown token " + tokens[0] + " when parsing MEASUREMENT")

    # TODO other parameters
    while tokens[0] != "/end" or tokens[1] != "MEASUREMENT":
        tokens = tokens[1:]

    return measurement, tokens[2:]


def record_layout(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "RECORD_LAYOUT":
        raise Exception("RECORD_LAYOUT expected, got " + tokens[0])

    name = tokens[1]
    tokens = tokens[1:]
    while tokens[0] != "/end" or tokens[1] != "RECORD_LAYOUT":
        tokens = tokens[1:]

    return A2LRecordLayout(name=name), tokens[2:]


def parse_value_charactersitics(tokens: list[str]) -> Tuple[Any, list[str]]:
    pass


def parse_array_characteristics(tokens: list[str]) -> Tuple[Any, list[str]]:
    pass


def characteristic(tokens: list[str]) -> Tuple[Any, list[str]]:
    if tokens[0] != "CHARACTERISTIC":
        raise Exception("CHARACTERISTIC expected, got " + tokens[0])

    name = tokens[1]
    description, tokens = parse_description(tokens[1:])

    characteristic_type = tokens[0]

    char_types = ["VALUE", "VAL_BLK", "ASCII", "CURVE", "MAP", "CUBOID", "CUBE_4"]

    if characteristic_type in char_types:
        pass
    else:
        raise Exception("Unknown characteristic type, got " + tokens[0])

    ecu_address = tokens[1]
    record_layout = tokens[2]
    some_int = tokens[3]
    something_else = tokens[4]
    min = tokens[5]
    max = tokens[6]

    tokens = tokens[7:]

    while tokens[0] != "/end" or tokens[1] != "CHARACTERISTIC":
        if tokens[0] == "EXTENDED_LIMITS":
            extended_min = tokens[1]
            extended_max = tokens[2]
            tokens = tokens[3:]
        elif tokens[0] == "FORMAT":
            format = tokens[1]
            tokens = tokens[2:]
        elif tokens[0] == "DISPLAY_IDENTIFIER":
            display_name = tokens[1]
            tokens = tokens[2:]
        elif tokens[0] == "BIT_MASK":
            bitmask = tokens[1]
            tokens = tokens[2:]
        elif tokens[0] == "MATRIX_DIM":
            matrix_dim, tokens = parse_matrix_dim(tokens)
        else:
            tokens = tokens[1:]
    return A2LCharacteristic(name=name, description=description), tokens[2:]


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
