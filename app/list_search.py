"""SQL helpers: single-field LIKE (search) and multi-value equality via IN (filter)."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from datetime import datetime
from typing import Any


def non_empty_strs(values: Iterable[str] | None) -> list[str]:
    if not values:
        return []
    return [v for v in values if v is not None and v != ""]


def compact_ints(values: Iterable[int] | None) -> list[int]:
    if not values:
        return []
    return [v for v in values if v is not None]


def compact_floats(values: Iterable[float] | None) -> list[float]:
    if not values:
        return []
    return [v for v in values if v is not None]


def compact_datetimes(values: Iterable[datetime] | None) -> list[datetime]:
    if not values:
        return []
    return [v for v in values if v is not None]


def append_in(clauses: list[str], params: list[Any], column_sql: str, vals: Sequence[Any]) -> None:
    if not vals:
        return
    placeholders = ", ".join(["%s"] * len(vals))
    clauses.append(f"({column_sql} IN ({placeholders}))")
    params.extend(vals)


def append_like(
    clauses: list[str], params: list[Any], column_sql: str, needle: str | None
) -> None:
    if needle is None or needle == "":
        return
    clauses.append(f"({column_sql} LIKE %s)")
    params.append(f"%{needle}%")
