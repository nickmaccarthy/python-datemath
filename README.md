[![Build Status](https://travis-ci.org/nickmaccarthy/python-datemath.svg?branch=master)](https://travis-ci.org/nickmaccarthy/python-datemath.svg?branch=master)


# What?
A date math (aka datemath) parser compatiable with the elasticsearch 'date math' format

# Why?
Working with date objects in python has always been interesting.  Having a background in php, I have been looking for quite some time ( no pun intended ) for a way to do date time interpolation similar to php's ```strtotime()``` function.  While the arrow module comes close, I needed something that could turn date math type strings into datetime objects for use in tattle.io and other projects I use in elasticsearch.  I have found even more uses for it, including AWS cloudwatch and various other projects and hopefully you will too.

# What is date math ?
Date Math is the short hand arithmetic to find relative time to fixed moments in date and time. Similar to the SOLR date math format, Elasticsearch has its own built in format for short hand date math and this module aims to support that same coverage in python.

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
now-2.5h                    2015-12-31T21:30:00+00:00
+2h                         2016-01-01T02:00:00+00:00
+1h/h                       2016-01-01T02:00:00+00:00
now+1w/w                    2016-01-11T00:00:00+00:00
now/d+7d+12h                2016-01-08T12:00:00+00:00
2016-01-01||+1d             2016-01-02T00:00:00+00:00
2015-01-01||+2w             2015-01-15T00:00:00+00:00

# Using the roundDown=False option
now/d                       2016-01-01T23:59:59+00:00
now/Y                       2016-12-31T23:59:59+00:00
```

# Usage
By default datemath return an arrow date object representing your timestamp.  

```
>>> from datemath import dm
>>>
>>> dm('now+1h')
<Arrow [2016-01-01T01:00:00+00:00]>
>>> dm('now+1h+1m')
<Arrow [2016-01-01T01:01:00+00:00]>
>>> dm('now+1h/d')
<Arrow [2016-01-02T00:00:00+00:00]>
>>> dm('now-1d')
<Arrow [2015-12-31T00:00:00+00:00]>
>>> dm('2016-01-01||+1/d')
<Arrow [2016-01-02T00:00:00+00:00]>
>>> dm('now/d+2h+3m')
<Arrow [2016-01-01T02:03:00+00:00]>
>>> dm('now+/d', roundDown=False)
<Arrow [2016-01-01T23:59:00+00:00]>
>>> dm('now/d')
<Arrow [2016-01-01T00:00:00+00:00]>
```

If you would rather have a string, you can use arrow's ```.format()``` method.
> For for info on string formatting, check out arrows tokens section: http://crsmithdev.com/arrow/#tokens
```
>>> from datemath import dm
>>>
>>> src_timestamp = dm('2016-01-01')
>>> print src_timestamp
2016-01-01T00:00:00+00:00
>>>
>>> new_timestamp = dm('-2w', now=src_timestamp)
>>> print new_timestamp
2015-12-18T00:00:00+00:00
>>>
>>> new_timestamp.format('YYYY.MM.DD')
u'2015.12.18'
>>>
```

Rather have a python datetime object instead? Just pass along the 'datetime' type
```
from datemath import dm
>>> dm('now', type='datetime')
datetime.datetime(2016, 1, 22, 22, 58, 28, 338060, tzinfo=tzutc())
>>>
>>> dm('now+2d-1m', type='datetime')
datetime.datetime(2016, 1, 24, 22, 57, 45, 394470, tzinfo=tzutc())
```

Or you can just import the `datamath` module, this will always give us a native `datetime` object
```
>>> from datemath import datemath
>>>
>>> datemath('2016-01-01T16:20:00||/d', roundDown=False)
datetime.datetime(2016, 1, 1, 23, 59, 59, 999999, tzinfo=tzutc())
>>>
>>>
>>> # roundDown=True is default and implied
>>> datemath('2016-01-01T16:20:00||/d')
datetime.datetime(2016, 1, 1, 0, 0, tzinfo=tzutc())
>>>
```

If you want a Epoch timestamp back instead, we can do that.  
```python
>>> dm('now+2d-1m', type='timestamp')
1453676321
```

# What timezone are my objects in?
By default all objects returned by datemath are in UTC.  If you want them them in a different timezone, just pass along the ```tz``` argument. 
Timezone list can be found here: https://gist.github.com/pamelafox/986163
```
from datemath import dm 
>>> dm('now')
<Arrow [2016-01-26T01:00:53.601088+00:00]>
>>>
>>> dm('now', tz='US/Eastern')
<Arrow [2016-01-25T20:01:05.976880-05:00]>
>>>
>>> dm('now', tz='US/Pacific')
<Arrow [2016-01-25T17:01:18.456882-08:00]>
>>>
>>> dm('2017-10-20 09:15:20', tz='US/Pacific')
<Arrow [2017-10-20T09:15:20.000000-08:00]>
```

# Release Notes
* v1.4.7 - Fixed timezone for date strings: https://github.com/nickmaccarthy/python-datemath/issues/6     
* v1.4.5 - Added roundDown functionality.  Allows user to specify the default rounding for expressions such as `/d`.
    * example - assuming the time is currently 2016-01-01 12:00:00, we should get the following
```
>>> # now = 2016-01-01 14:00:00+00:00
>>> dm('now+/d', roundDown=False)
<Arrow [2016-01-01T23:59:00+00:00]>
>>> dm('now/d')
<Arrow [2016-01-01T00:00:00+00:00]>
```   
* v1.4.4 - Fixed bug with expression logic and rounding:  https://github.com/nickmaccarthy/python-datemath/pull/2
* v1.4.3 - Floats are now supported for days, hours, and seconds units.  Example ```now-2.5d```, ```now-3.2h```. Any other unit other than days, hours, or seconds that is a float will be converted to an int and floored due to the datetime() module not being able to handle them.

# Test
```python tests.py```

Happy date math'ing!

