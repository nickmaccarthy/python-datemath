from __future__ import annotations

from datetime import datetime
from typing import Any

from arrow import Arrow

from ._version import __version__
from .helpers import DateMathException as DateMathException
from .helpers import parse as parse


def dm(expr: str | int, **kwargs: Any) -> Arrow:
    """Apply date math and return the requested output type."""
    return parse(expr, **kwargs)


def datemath(expr: str | int, **kwargs: Any) -> datetime:
    """Apply date math and return a standard ``datetime`` object."""
    return parse(expr, **kwargs).datetime


__all__ = [
    "dm",
    "datemath",
    "parse",
    "DateMathException",
    "__version__",
]
