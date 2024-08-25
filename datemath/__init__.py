from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from arrow import Arrow

if TYPE_CHECKING:
    from typing_extensions import Unpack

from .helpers import ParseParams, parse as parse, DateMathException as DateMathException

def dm(expr: str | int, **kwargs: Unpack[ParseParams]) -> Arrow:
    ''' does our datemath and returns an arrow object '''
    return parse(expr, **kwargs)

def datemath(expr: str | int, **kwargs: Unpack[ParseParams]) -> datetime:
    ''' does our datemath and returns a datetime object '''
    return parse(expr, **kwargs).datetime
