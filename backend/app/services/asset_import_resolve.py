"""Resolve FK values from import cells (numeric ID, dropdown 'id - name', or name lookup)."""
import re
from typing import Any, Callable, Optional


def parse_id_value(value: Any) -> Optional[int]:
    """Parse cell to integer ID: 5, '5', '5 - Label', 5.0"""
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value) if value == int(value) else None
    s = str(value).strip()
    if not s:
        return None
    if " - " in s:
        s = s.split(" - ", 1)[0].strip()
    if re.match(r"^\d+$", s):
        return int(s)
    try:
        f = float(s)
        if f == int(f):
            return int(f)
    except ValueError:
        pass
    return None


def resolve_fk(
    value: Any,
    lookup_by_id: Callable[[int], bool],
    lookup_by_name: Callable[[str], Optional[int]],
) -> Optional[int]:
    """
    Returns resolved ID or None if empty.
    Raises ValueError if value provided but not found.
    """
    if value is None or str(value).strip() == "":
        return None
    pid = parse_id_value(value)
    if pid is not None:
        if lookup_by_id(pid):
            return pid
        raise ValueError(f"ID {pid} not found")
    name = str(value).strip()
    found = lookup_by_name(name)
    if found is not None:
        return found
    raise ValueError(f"'{name}' not found")


def parse_stockid(value: Any) -> Optional[list]:
    """stockid column: single id, comma list, or '{3,4}'"""
    if value is None or str(value).strip() == "":
        return None
    s = str(value).strip()
    if " - " in s:
        s = s.split(" - ", 1)[0].strip()
    s = s.strip("{}[]")
    parts = [p.strip() for p in s.replace(";", ",").split(",") if p.strip()]
    ids = []
    for p in parts:
        pid = parse_id_value(p)
        if pid is not None:
            ids.append(pid)
        else:
            raise ValueError(f"Invalid stockid '{p}'")
    return ids if ids else None
