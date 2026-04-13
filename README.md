# Python Datemath

<p align="center">
  Parse Elasticsearch-style date math in Python with clean timezone-aware results.
</p>

<p align="center">
  <a href="https://pypi.org/project/python-datemath/"><img alt="PyPI" src="https://img.shields.io/pypi/v/python-datemath.svg"></a>
  <a href="https://pypi.org/project/python-datemath/"><img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/python-datemath.svg"></a>
  <a href="https://github.com/nickmaccarthy/python-datemath/actions/workflows/ci.yaml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/nickmaccarthy/python-datemath/ci.yaml?branch=master"></a>
  <a href="https://pypi.org/project/python-datemath/"><img alt="License" src="https://img.shields.io/pypi/l/python-datemath.svg"></a>
</p>

Date math is the compact syntax used by systems like Elasticsearch, Splunk and Solr for expressions such as `now-15m`, `now/d`, or `2024-01-01||+1M`. `python-datemath` brings that same style to Python and returns proper timezone-aware values you can keep as `Arrow`, convert to `datetime`, or render as timestamps.

## Why use it?

- Familiar Elasticsearch, Splunk, Datadog and Solr-style expressions
- Timezone-aware parsing and arithmetic
- Support for rounding like `/d`, `/w`, and `/M`
- Works with `Arrow`, `datetime`, and unix timestamps
- Small library, simple API, no framework required

## Quick Start

```bash
pip install python-datemath
```

Python `3.10+` is supported.

```python
from datemath import dm, datemath

print(dm("now-15m"))
print(dm("now/d+8h"))
print(datemath("2024-01-01||+1M"))
print(dm("now", tz="US/Eastern"))
```

## At A Glance

```text
now-1h                  one hour ago
now+1d/d                tomorrow, rounded to the start of day
now/w+2d                two days after the start of this week
2024-01-01||+1M         one month after an anchored date
2024-01-01||/M          start of that month
2024-01-01T12:00:00-05:00||+2h
                        preserve an explicit offset from the source string
```

## What Is Date Math?

Date math is shorthand arithmetic for finding times relative to a fixed moment.

An expression is made of:

1. An anchor, either `now` or a timestamp ending in `||`
2. Zero or more operations using `+`, `-`, or `/`
3. A supported time unit such as year, month, week, day, hour, minute, or second

Examples:

- `now+1h`
- `now+1h+1m`
- `now+1h/d`
- `2012-01-01||+1M/d`

When `roundDown=False`, rounding uses the end of the interval instead of the beginning.

## Supported Units

```text
y or Y   year
M        month
w or W   week
d or D   day
h or H   hour
m        minute
s or S   second
now      current date and time
```

## Usage

### Return an `Arrow` object

`dm()` returns an `Arrow` object by default.

```python
>>> from datemath import dm
>>>
>>> dm("now+1h")
<Arrow [2016-01-01T01:00:00+00:00]>
>>> dm("now+1h+1m")
<Arrow [2016-01-01T01:01:00+00:00]>
>>> dm("now+1h/d")
<Arrow [2016-01-02T00:00:00+00:00]>
>>> dm("now-1d")
<Arrow [2015-12-31T00:00:00+00:00]>
>>> dm("2016-01-01||+1/d")
<Arrow [2016-01-02T00:00:00+00:00]>
>>> dm("now/d+2h+3m")
<Arrow [2016-01-01T02:03:00+00:00]>
>>> dm("now+/d", roundDown=False)
<Arrow [2016-01-01T23:59:00+00:00]>
>>> dm("now/d")
<Arrow [2016-01-01T00:00:00+00:00]>
>>> dm(1451610061)
<Arrow [2016-01-01T01:01:01+00:00]>
>>> dm("1451610061")
<Arrow [2016-01-01T01:01:01+00:00]>
```

If you want a string, use Arrow's `.format()` method.

```python
>>> from datemath import dm
>>>
>>> src_timestamp = dm("2016-01-01")
>>> src_timestamp
<Arrow [2016-01-01T00:00:00+00:00]>
>>>
>>> new_timestamp = dm("-2w", now=src_timestamp)
>>> new_timestamp
<Arrow [2015-12-18T00:00:00+00:00]>
>>>
>>> new_timestamp.format("YYYY.MM.DD")
'2015.12.18'
```

### Return a standard `datetime`

Use `datemath()` if you want a standard Python `datetime`.

```python
>>> from datemath import datemath
>>>
>>> datemath("now-1h")
datetime.datetime(2015, 12, 31, 23, 0, tzinfo=tzutc())
>>> str(datemath("now-1h"))
'2015-12-31 23:00:00+00:00'
>>> datemath("2016-01-01T16:20:00||/d")
datetime.datetime(2016, 1, 1, 0, 0, tzinfo=tzutc())
>>> datemath("2016-01-01T16:20:00||/d", roundDown=False)
datetime.datetime(2016, 1, 1, 23, 59, 59, 999999, tzinfo=tzutc())
```

You can also use `dm()` with `type="datetime"`:

```python
>>> from datemath import dm
>>>
>>> dm("now", type="datetime")
datetime.datetime(2016, 1, 22, 22, 58, 28, 338060, tzinfo=tzutc())
>>> dm("now+2d-1m", type="datetime")
datetime.datetime(2016, 1, 24, 22, 57, 45, 394470, tzinfo=tzutc())
```

### Return a unix timestamp

```python
>>> from datemath import dm
>>>
>>> dm("now+2d-1m", type="timestamp")
1453676321
```

## Timezones

By default, returned values are in UTC.

If you want a different timezone, pass the `tz` argument:

```python
>>> from datemath import dm
>>>
>>> dm("now")
<Arrow [2016-01-26T01:00:53.601088+00:00]>
>>> dm("now", tz="US/Eastern")
<Arrow [2016-01-25T20:01:05.976880-05:00]>
>>> dm("now", tz="US/Pacific")
<Arrow [2016-01-25T17:01:18.456882-08:00]>
>>> dm("2017-10-20 09:15:20", tz="US/Pacific")
<Arrow [2017-10-20T09:15:20.000000-08:00]>
```

If a timestamp string already contains an explicit timezone offset, that offset is preserved:

```python
>>> dm("2016-01-01T00:00:00-05:00")
<Arrow [2016-01-01T00:00:00-05:00]>
>>> dm("2016-01-01T00:00:00-05:00||+2d+3h+5m")
<Arrow [2016-01-03T03:05:00-05:00]>
>>> dm("2016-01-01T00:00:00-05:00", tz="US/Central")
<Arrow [2016-01-01T00:00:00-05:00]>
```

## More Examples

Assuming our current time is `2016-01-01T00:00:00+00:00`:

```shell
Expression                 Result
now-1h                     2015-12-31T23:00:00+00:00
now-1y                     2015-01-01T00:00:00+00:00
now+1y+2d                  2017-01-03T00:00:00+00:00
now+12h                    2016-01-01T12:00:00+00:00
now+1d/d                   2016-01-03T00:00:00+00:00
now-2.5h                   2015-12-31T21:30:00+00:00
+2h                        2016-01-01T02:00:00+00:00
+1h/h                      2016-01-01T02:00:00+00:00
now+1w/w                   2016-01-11T00:00:00+00:00
now/d+7d+12h               2016-01-08T12:00:00+00:00
2016-01-01||+1d            2016-01-02T00:00:00+00:00
2015-01-01||+2w            2015-01-15T00:00:00+00:00

roundDown=False
now/d                      2016-01-01T23:59:59+00:00
now/Y                      2016-12-31T23:59:59+00:00
```

## Installation Options

### Install from PyPI

```bash
pip install python-datemath
```

### Install in a project with `uv`

```bash
uv add python-datemath
```

### Install for local development

```bash
uv sync --group dev
```

## Development

This project uses [`pyproject.toml`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) for packaging and [`uv`](https://docs.astral.sh/uv/) for local workflows.

```bash
uv sync --group dev
uv run pytest
uv run ruff check .
uv run mypy
uv build
```

If you prefer `make`, the common tasks are wrapped there too:

```bash
make sync
make check
make build
```

## Debugging

If you want verbose debug output, set `DATEMATH_DEBUG=true` in your shell before running examples or tests:

```bash
export DATEMATH_DEBUG=true
uv run pytest
unset DATEMATH_DEBUG
```

## Changes

See [CHANGELOG.md](./CHANGELOG.md).

---

Built for people who think that dates and time should be easier to use in python
