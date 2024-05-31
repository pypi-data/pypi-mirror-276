import re
from typing import Optional


def is_alphanumeric(s: Optional[str]) -> bool:
    if s is None:
        raise ValueError("Input cannot be None")
    if not isinstance(s, str):
        raise ValueError("Input must be a string")
    return bool(re.match("^[a-zA-Z0-9]*$", s))
