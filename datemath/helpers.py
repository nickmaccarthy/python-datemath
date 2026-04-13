from __future__ import annotations

import os
import re
from datetime import timedelta
from typing import TypedDict, cast

import arrow
from arrow import Arrow

debug = bool(os.environ.get("DATEMATH_DEBUG"))

UNIT_ALIASES = {
    "y": "years",
    "Y": "years",
    "year": "years",
    "years": "years",
    "M": "months",
    "month": "months",
    "months": "months",
    "m": "minutes",
    "minute": "minutes",
    "minutes": "minutes",
    "d": "days",
    "D": "days",
    "day": "days",
    "days": "days",
    "w": "weeks",
    "W": "weeks",
    "week": "weeks",
    "weeks": "weeks",
    "h": "hours",
    "H": "hours",
    "hour": "hours",
    "hours": "hours",
    "s": "seconds",
    "S": "seconds",
    "second": "seconds",
    "seconds": "seconds",
}

HAS_TIMEZONE_SUFFIX = re.compile(r"(Z|[+-]\d{2}:\d{2})$")


class DateMathException(Exception):
    pass


def unitMap(c: str) -> str:
    """
    Map supported time unit aliases to the names expected by Arrow.
    """
    if c.lower() in {"n", "now"}:
        raise DateMathException(
            f'Timeunit: "{c}" is not valid. If you are trying to specify "now" '
            "after a timestamp (for example, 2016-01-01||now/d) that is not valid. "
            'Please try "2016-01-01||/d" instead.'
        )

    try:
        return UNIT_ALIASES[c]
    except KeyError as exc:
        raise DateMathException(f"Not a valid timeunit: {c}") from exc

class ParseParams(TypedDict, total=False):
    now: Arrow | None
    tz: str
    type: str | None
    roundDown: bool


def parse(
    expression: str | int,
    now: Arrow | None = None,
    tz: str = "UTC",
    type: str | None = None,
    roundDown: bool = True,
) -> Arrow:
    """
    Parse a date math expression and return the evaluated value.
    """
    if debug:
        print(f"parse() - starting for expression: {expression}")
    if now is None:
        if debug:
            print("parse() - Now is None, setting now to utcnow()")
        now = arrow.utcnow()

    if debug:
        print(f"parse() - Orig Expression: {expression}")

    math = ""
    time = None

    if tz != "UTC":
        if debug:
            print(f"parse() - will now convert tz to {tz}")
        now = now.to(tz)

    expression = str(expression)
    if expression == "now":
        if debug:
            print(f"parse() - Now, no dm: {now}")
        if type:
            return cast(Arrow, getattr(now, type))
        return now
    if re.match(r"\d{10,}", expression):
        if debug:
            print("parse() - found an epoch timestamp")
        if len(expression) == 13:
            raise DateMathException(
                "Unable to parse epoch timestamps in millis, please convert to the "
                "nearest second to continue - i.e. 1451610061 / 1000"
            )
        ts = arrow.get(int(expression))
        ts = ts.replace(tzinfo=tz)
        return ts
    if expression.startswith("now"):
        # Parse standard "now+1d" expressions.
        math = expression[3:]
        time = now
        if debug:
            print(f"parse() - now expression: {now}")
    else:
        # Parse anchored expressions like "2015-10-20||+1d".
        if "||" in expression:
            timestamp, math = expression.split("||")
            time = parseTime(timestamp, tz)
        elif expression.startswith(("+", "-", "/")):
            # These expressions are implicitly relative to "now".
            math = expression
            time = now
        else:
            if debug:
                print("parse() - Found an expression that will hit the catchall")
            math = ""
            time = parseTime(expression, tz)

    if not math:
        rettime = time
    else:
        rettime = evaluate(math, time, tz, roundDown)

    if type is not None:
        return cast(Arrow, getattr(rettime, type))
    return rettime
        

def parseTime(timestamp: str, timezone: str = "UTC") -> Arrow:
    """
    Parse a timestamp string into an ``Arrow`` instance.
    """
    if timestamp and len(timestamp) >= 4:
        ts = arrow.get(timestamp)
        if debug:
            print(f"parseTime() - ts = {ts} :: vars :: {vars(ts)}")
            print(f"parseTime() - ts timezone = {ts.tzinfo}")
            print(f"parseTime() - tzinfo type = {type(ts.tzinfo)}")
            print(f"parseTime() - timezone that came in = {timezone}")

        if HAS_TIMEZONE_SUFFIX.search(timestamp):
            # Preserve an explicit offset or "Z" suffix from the source timestamp.
            return ts

        if ts.tzinfo is None or ts.tzinfo.utcoffset(ts.datetime) == timedelta(0):
            # Otherwise, ensure the parsed timestamp uses the requested timezone.
            ts = ts.replace(tzinfo=timezone)

        return ts
    if debug:
        print(
            "parseTime() - Doesnt look like we have a valid timestamp, raise an exception. "
            f"timestamp={timestamp}"
        )
    raise DateMathException(
        f'Valid length timestamp not provide, you gave me a timestamp of "{timestamp}", '
        "but I need something that has a len() >= 4"
    )


def roundDate(now: Arrow, unit: str, tz: str = "UTC", roundDown: bool = True) -> Arrow:
    """
    Round a date object to the requested unit.
    """
    if roundDown:
        now = now.floor(unit)  # type: ignore[arg-type]
    else:
        now = now.ceil(unit)  # type: ignore[arg-type]
    if debug:
        print(f"roundDate() Now: {now}")
    return now


def calculate(now: Arrow, offsetval: float, unit: str) -> Arrow:
    """
    Shift a date object by the requested unit and value.
    """
    if unit not in {"days", "hours", "seconds"}:
        offsetval = int(offsetval)
    try:
        now = now.shift(**cast(dict[str, int | float], {unit: offsetval}))  # type: ignore[arg-type]
        if debug:
            print(
                f"calculate() called:  now: {now}, offsetval: {offsetval}, "
                f"offsetval-type: {type(offsetval)}, unit: {unit}"
            )
        return now
    except Exception as e:
        raise DateMathException(
            f"Unable to calculate date: now: {now}, offsetvalue: {offsetval}, "
            f"unit: {unit} - reason: {e}"
        ) from e


def evaluate(expression: str, now: Arrow, timeZone: str = "UTC", roundDown: bool = True) -> Arrow:
    """
    Evaluate a date math expression against an Arrow timestamp.
    """
    if debug:
        print(f"evaluate() - Expression: {expression}")
        print(f"evaluate() - Now: {now}")
    val = float(0)
    i = 0
    while i < len(expression):
        char = expression[i]

        if "/" in char:
            next = str(expression[i+1])
            i += 1
            now = roundDate(now, unitMap(next).rstrip("s"), timeZone, roundDown)

        elif char == "+" or char == "-":
            val = 0

            try:
                m = re.match(r"(\d*[.]?\d+)[\w+-/]", expression[i + 1 :])
                if m:
                    num = m.group(1)
                    val = val * 10 + float(num)
                    i = i + len(num)
                else:
                    raise DateMathException(
                        "Unable to determine a proper time qualifier. Do you have a "
                        "proper numerical number followed by a valid time unit? "
                        "i.e. '+1d', '-3d/d', etc."
                    )
            except Exception as e:
                raise DateMathException(
                    f"Invalid datematch: What I got was - re.match: {expression[i + 1 :]}, "
                    f"expression: {expression}, error: {e}"
                ) from e
    
            if char == "+":
                val = float(val)
            else:
                val = float(-val)
        elif re.match(r"[a-zA-Z]+", char):
            now = calculate(now, val, unitMap(char))
        else:
            raise DateMathException(
                f"'{char}' is not a valid timeunit for expression: '{expression}'"
            )
        
        i += 1
    if debug:
        print(f"evaluate() - Finished: {now}")
        print("\n\n")
    return now
