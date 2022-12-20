import re
from typing import Union


def get_number(key: str) -> int:
    pattern = r"^(?P<number>\d{1,2})"
    result = re.search(pattern, key)
    if result:
        return int(result.group("number"))
    else:
        raise ValueError(f"'string' not in correct format, 'string' is {key!r}")


def get_letter(key: str) -> Union[str, None]:
    pattern = r"(?P<letter>[A-Z]?)$"
    result = re.search(pattern, key)
    if result:
        return result.group("letter")
    else:
        return None


def get_tag(number: int) -> str:
    if 1 <= number <= 17 or 52 <= number <= 58:
        return "home"
    elif number == 18:
        return "center"
    elif 19 <= number <= 50 or 59 <= number <= 80:
        return "system"
    elif 83 <= number <= 91:
        return "hyperlane"
    elif number == 51 or number == 81 or number == 82:
        return "exterior"
    else:
        raise ValueError(f"number must be between 1 and 91, not {number}")
