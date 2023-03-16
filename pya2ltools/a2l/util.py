def is_number(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False
