[![Build Status](https://travis-ci.org/nickmaccarthy/python-datemath.svg?branch=master)](https://travis-ci.org/nickmaccarthy/python-datemath.svg?branch=master)


# What?
A date match parser to be compatiable with the elasticsearch date math format

# Why?
Working with date objects in python has always been interesting.  Having a background in php, I have been looking for quite some time ( no pun intended ) for a way to do date time interpolation similar to php's ```strtotime()``` function.  While the arrow module comes close, I needed something that could turn math type strings into datetime objects for use in tattle.io and other projects I use in elasticsearch.  I have found even more uses for it, and hopefully you will to.

# What is date math ?
Similar to the SOLR date math format, elasticsearch has its own built in format for short hand date math.  This module aims to support that same coverage in python.

Documentation from elasticsearch:
http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/mapping-date-format.html#date-math

> The date type supports using date math expression when using it in a query/filter (mainly makes sense in range query/filter).

> The expression starts with an "anchor" date, which can be either now or a date string (in the applicable format) ending with `||`.

> It can then follow by a math expression, supporting `+`, `-` and `/` (rounding).

> The units supported are `y` (year), `M` (month), `w` (week), `d` (day), `h` (hour), `m` (minute), and `s` (second).

> Here are some samples: `now+1h`, `now+1h+1m`, `now+1h/d`, `2012-01-01||+1M/d`.

> Note, when doing range type searches, and the upper value is inclusive, the rounding will properly be rounded to the ceiling instead of flooring it.

# Unit Maps
```
y or Y      =   'year'
M           =   'month'
m           =   'minute'
d or D      =   'day'
w           =   'week'
h or H      =   'hour'
s or S      =   'second'
```

# Install
```python
pip install python-datemath
```
# Examples
Assuming our datetime is currently: '2016-01-01T00:00:00-00:00'
```
Expression:                 Result:
now-1h                      2015-12-31T23:00:00+00:00
now-1y                      2015-01-01T00:00:00+00:00
now+1y+2d                   2017-01-03T00:00:00+00:00
now+12h                     2016-01-01T12:00:00+00:00
now+1d/d                    2016-01-03T00:00:00+00:00
+2h                         2016-01-01T02:00:00+00:00
+1h/h                       2016-01-01T02:00:00+00:00
now+1w/w                    2016-01-11T00:00:00+00:00
now/d+7d+12h                2016-01-08T12:00:00+00:00
2016-01-01||+1d             2016-01-02T00:00:00+00:00
2015-01-01||+2w             2015-01-15T00:00:00+00:00
```

# Usage
By default datemath return an arrow date object representing your timestamp.  

```python
>>> import datemath as dm
>>>
>>> dm.parse('now+1h')
<Arrow [2016-01-01T01:00:00+00:00]>
>>> dm.parse('now+1h+1m')
<Arrow [2016-01-01T01:01:00+00:00]>
>>> dm.parse('now+1h/d')
<Arrow [2016-01-02T00:00:00+00:00]>
>>> dm.parse('now-1d')
<Arrow [2015-12-31T00:00:00+00:00]>
>>> dm.parse('2016-01-01||+1/d')
<Arrow [2016-01-02T00:00:00+00:00]>
>>> dm.parse('now/d+2h+3m')
<Arrow [2016-01-01T02:03:00+00:00]>
>>>
```
If you would rather have a string, you can arrow's ```.format()``` method.
> For for info on string formatting, check out arrows tokens section: http://crsmithdev.com/arrow/#tokens
```python
>>> import datemath as dm
>>>
>>> src_timestamp = dm.parse('2016-01-01')
>>> print src_timestamp
2016-01-01T00:00:00+00:00
>>>
>>> new_timestamp = dm.parse('-2w', now=src_timestamp)
>>> print new_timestamp
2015-12-18T00:00:00+00:00
>>>
>>> new_timestamp.format('YYYY.MM.DD')
u'2015.12.18'
>>>
```

If you would rather have a datetime object instead, pass along the 'datetime' type
```python
>>> dm.parse('now', type='datetime')
datetime.datetime(2016, 1, 22, 22, 58, 28, 338060, tzinfo=tzutc())
>>>
>>> dm.parse('now+2d-1m', type='datetime')
datetime.datetime(2016, 1, 24, 22, 57, 45, 394470, tzinfo=tzutc())
```
Rather have an Epoch/Unix Timestamp back instead? Pass along 'timestamp' type
```python
>>> dm.parse('now+2d-1m', type='timestamp')
1453676321
```

# Test
```python tests.py```


This was inspired by the npm datemath-parser written by randing89
https://github.com/randing89/datemath-parser
