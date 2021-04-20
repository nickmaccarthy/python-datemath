# Changelog

## 1.5.3 (2021-04-16)
* [FIX] [Issue #25](https://github.com/nickmaccarthy/python-datemath/issues/25) - Fixed an issue where if you provided an invalid timestamp, i.e. `datemath('2')` you would not get an DateMathException back.  Also bumped dependencies.

## 1.5.2 (2020-10-01)
* [FIX] [Issue #21](https://github.com/nickmaccarthy/python-datemath/issues/21) - Fixed an issue where if timezone offset was in a datetime string (ISO8601), the timezone of the returned datemath object would be UTC and not the timezone as specified in the datetime string.

## 1.5.1 (2020-03-25)

* [FIX] [Issue #15](https://github.com/nickmaccarthy/python-datemath/issues/15) - Fixed issue with parser finding invalid timeunits and throwing correct errors
* [NEW] [Issue #16](https://github.com/nickmaccarthy/python-datemath/issues/16) - Added support for parser to accecpt a epoch/unix timestamp but throw an error on epoch milli's since arrow can't support that.  

## 1.5.0 (2019-11-09)

* [FIX] [Issue #12](https://github.com/nickmaccarthy/python-datemath/issues/12) - missing VERSION.txt.  Added MANIFEST.in for sdist build
* [FIX] [PR #13](https://github.com/nickmaccarthy/python-datemath/pull/13) - Fix `BaseException` to `Exception` inheritence, thank you for your contribution @yury-primer!

## 1.4.9 (2019-10-26)

** PLEASE DO NOT USE THIS VERSION, use `1.5.0+` instead.  This may not compile on your system due to a missing VERSION.txt which was fixed in `1.5.0+` **
* [FIX] [Issue #9](https://github.com/nickmaccarthy/python-datemath/issues/9) && [Issue #8](https://github.com/nickmaccarthy/python-datemath/issues/8) - Fixing deprecated arrow `replace()` function with `shift()`.
* [FIX] Arrow upgrade to `0.15.2` to fix the above mentioned issues
* [NEW] Breakout of python2 and python3 requirements
* [NEW] Breakout of python2 and python3 specific CICD pipelines
* [NEW] Derecated the following python version (although they may still work, they are no longer supported) - `2.4`,`2.6`,`3.4`,`3.5`
* [FIX] Modifed `tests.py` to account for the timestamp change (tz is now `+0000`, instead of `-0000`)
* [FIX] replaced `ts = ts.replace(tzinfo=tz.gettz(timezone))` with `ts = ts.replace(tzinfo=timezone)` in `datemath.helpers.parseTime()` to fix [Issue #7](https://github.com/nickmaccarthy/python-datemath/issues/7)

## v1.4.8 (2019-10-25)
* skipped due to name conflict on pypi, all changes are in `1.4.9`

## v1.4.7 (2017-11-10)
* [FIX] Fixed timezone for date strings: [Issue #6](https://github.com/nickmaccarthy/python-datemath/issues/6)

## v1.4.5 (2017-03-21)
* [NEW] Added roundDown functionality.  Allows user to specify the default rounding for expressions such as `/d`.
* example - assuming the time is currently 2016-01-01 12:00:00, we should get the following
```
>>> # now = 2016-01-01 14:00:00+00:00
>>> dm('now+/d', roundDown=False)
<Arrow [2016-01-01T23:59:00+00:00]>
>>> dm('now/d')
<Arrow [2016-01-01T00:00:00+00:00]>
```   

## v1.4.4 (2016-12-28)
* [FIX] Fixed bug with expression logic and rounding:  https://github.com/nickmaccarthy/python-datemath/pull/2

## 1.4.3 (2016-03-31)
* [NEW] Floats are now supported for days, hours, and seconds units.  Example ```now-2.5d```, ```now-3.2h```. Any other unit other than days, hours, or seconds that is a float will be converted to an int and floored due to the datetime() module not being able to handle them.