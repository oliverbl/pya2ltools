from typing import Any, Callable, Tuple


def is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def parse_number(s: str) -> int:
    if s.startswith("0x"):
        return int(s, 16)
    if s.startswith("0b"):
        return int(s, 2)
    if s.startswith("0o"):
        return int(s, 8)
    try:
        return int(s)
    except ValueError:
        return float(s)


def parse_string(tokens: list[str]) -> Tuple[str, list[str]]:
    if tokens[0].startswith('"') and tokens[0].endswith('"'):
        return tokens[0][1:-1], tokens[1:]

    description = tokens[0][1:] + " "
    tokens = tokens[1:]

    while not tokens[0].endswith('"'):
        description += tokens[0] + " "
        tokens = tokens[1:]

    description += tokens[0][:-1]

    return description, tokens[1:]

def parse_members(
    tokens: list[str], field: str, name: str
) -> Tuple[dict, list[str]]:
    members = []
    tokens = tokens[1:]
    while tokens[0] != "/end" or tokens[1] != name:
        members.append(tokens[0])
        tokens = tokens[1:]
    return {field: members}, tokens[2:]

# a lexing function takes a list of tokens and returns a dictionary of str to Object and sublist of the tokens, after processing
Lexer_Func = Callable[[list[str]], Tuple[dict[str, Any], list[str]]]

Lexer = dict[str, Lexer_Func]


def add_key_values(key_value: dict, params: dict) -> None:
    for k, v in key_value.items():
        if isinstance(v, list):
            if k not in params:
                params[k] = []
            params[k] += v
        else:
            params[k] = v


def parse_with_lexer(
    lexer: Lexer, name: str, params: dict[str, Any], tokens: list[str]
) -> list[str]:
    while tokens[0] != "/end" or tokens[1] != name:
        func = lexer.get(tokens[0], None)
        if func is None:
            print(tokens[:20])
            raise Exception(f"Unknown token  {tokens[0]} when parsing {name}")
        key_value, tokens = func(tokens)
        add_key_values(key_value, params)
    return tokens[2:]
