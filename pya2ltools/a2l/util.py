def is_number(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False

def parse_int(s: str) -> int:
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