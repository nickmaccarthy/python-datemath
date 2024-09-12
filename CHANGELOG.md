# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.3] - 2024-09-12
Please use 3.0.3 going forward!   3.0.2 has a breaking bug.

### fixed
- Fix: issue where version wasnt getting populated
- Fix: move version out of `VERSION.txt` and into `datemath/_version.py` directly
- Fix: typos in CHANGELOG.  Thank you @s00hyun!

## [3.0.2] - 2024-09-11
### added
- Feat: Complete typing with strict type-checking [#43](https://github.com/nickmaccarthy/python-datemath/pull/43) Thank you @Avasam!
- Feat: Added `__version__` to verify the version of the module.  
- Feat: Added Dockerfile and relevant verify.py to help with local development and testing

### chore
- Chore: bumped modules in requirements.txt

### fixed
- Fix: removed legacy-tests.py since we no longer support python2.x
- Fix: removed requirements-2.txt from manifest due to deprecation of python2 support
- Fix: renamed requirements-3.txt to requirements.txt to support python3 going forward
    - also modifed to `release.yaml` and `tests.yaml` workflows to support this
- Fix: long_description should now show up in pypi https://github.com/nickmaccarthy/python-datemath/issues/33
- Fix: move more pypi configurations to setup.cfg and out of setup.py


## [3.0.1] - 2024-08-23 
### fixed
- Fix: Race condition in timezone tests: https://github.com/nickmaccarthy/python-datemath/issues/36
- Fix: Updated arrow version: https://github.com/nickmaccarthy/python-datemath/issues/32
- Fix: mypy type hint checking in tests: https://github.com/nickmaccarthy/python-datemath/issues/31 
- Fix: SyntaxWarning: invalid escape sequence in `re.match()`: https://github.com/nickmaccarthy/python-datemath/pull/39
- Fix: Licence Classifier: https://github.com/nickmaccarthy/python-datemath/pull/34
- Fix: Bump certifi to latest: https://github.com/nickmaccarthy/python-datemath/pull/38
### added 
- Feat: Typehint support: https://github.com/nickmaccarthy/python-datemath/issues/31
- Feat: Renamed CHANGELOG.md to keepachangelog.org format

### todo
- todo: Fix pypi: https://github.com/nickmaccarthy/python-datemath/issues/33

## deprecated
- python 2.7 support. Python 3.8+ will only be supported going forward

## [1.5.5] - 2021-04-26
### fixed 
- fix: [Issue #28](https://github.com/nickmaccarthy/python-datemath/issues/28)
    * `datemath()` object now returns the expected `datetime` object instead of an `Arrow` object
    * added tests to catch invalid object types of helpers

## [1.5.4] - 2021-04-20
### Unused 
- skipped due to name conflict on pypi, all changes in this are from `1.5.3`

## [1.5.3] - 2021-04-16
### fixed
- FIX: [Issue #25](https://github.com/nickmaccarthy/python-datemath/issues/25) - Fixed an issue where if you provided an invalid timestamp, i.e. `datemath('2')` you would not get an DateMathException back.  Also bumped dependencies.

## [1.5.2] - 2020-10-01
### fixed
- FIX: [Issue #21](https://github.com/nickmaccarthy/python-datemath/issues/21) - Fixed an issue where if timezone offset was in a datetime string (ISO8601), the timezone of the returned datemath object would be UTC and not the timezone as specified in the datetime string.

## [1.5.1] -  2020-03-25

### fixed
- FIX: [Issue #15](https://github.com/nickmaccarthy/python-datemath/issues/15) - Fixed issue with parser finding invalid timeunits and throwing correct errors
### added
- Feat: [Issue #16](https://github.com/nickmaccarthy/python-datemath/issues/16) - Added support for parser to accecpt a epoch/unix timestamp but throw an error on epoch milli's since arrow can't support that.  

## [1.5.0] - 2019-11-09

### fixed
- [Issue #12](https://github.com/nickmaccarthy/python-datemath/issues/12) - missing VERSION.txt.  Added MANIFEST.in for sdist build
- [PR #13](https://github.com/nickmaccarthy/python-datemath/pull/13) - Fix `BaseException` to `Exception` inheritence, thank you for your contribution @yury-primer!

## [1.4.9] - 2019-10-26

** PLEASE DO NOT USE THIS VERSION, use `1.5.0+` instead.  This may not compile on your system due to a missing VERSION.txt which was fixed in `1.5.0+` **

### fixed 
- [FIX] [Issue #9](https://github.com/nickmaccarthy/python-datemath/issues/9) && [Issue #8](https://github.com/nickmaccarthy/python-datemath/issues/8) - Fixing deprecated arrow `replace()` function with `shift()`.
- [FIX] Arrow upgrade to `0.15.2` to fix the above mentioned issues
- [FIX] Modifed `tests.py` to account for the timestamp change (tz is now `+0000`, instead of `-0000`)
- [FIX] replaced `ts = ts.replace(tzinfo=tz.gettz(timezone))` with `ts = ts.replace(tzinfo=timezone)` in `datemath.helpers.parseTime()` to fix [Issue #7](https://github.com/nickmaccarthy/python-datemath/issues/7)
### added

- [NEW] Breakout of python2 and python3 requirements
- [NEW] Breakout of python2 and python3 specific CICD pipelines
- [NEW] Derecated the following python version (although they may still work, they are no longer supported) - `2.4`,`2.6`,`3.4`,`3.5`


## [1.4.8] - 2019-10-25
** dont use this version **
* skipped due to name conflict on pypi, all changes are in `1.4.9`

## [1.4.7] - 2017-11-10
### fixed 
- [FIX] Fixed timezone for date strings: [Issue #6](https://github.com/nickmaccarthy/python-datemath/issues/6)

## [1.4.5] - 2017-03-21
### added
- [NEW] Added roundDown functionality.  Allows user to specify the default rounding for expressions such as `/d`.
- example - assuming the time is currently 2016-01-01 12:00:00, we should get the following
```
>>> # now = 2016-01-01 14:00:00+00:00
>>> dm('now+/d', roundDown=False)
<Arrow [2016-01-01T23:59:00+00:00]>
>>> dm('now/d')
<Arrow [2016-01-01T00:00:00+00:00]>
```   

## [1.4.4] - 2016-12-28
### fixed
- [FIX] Fixed bug with expression logic and rounding:  https://github.com/nickmaccarthy/python-datemath/pull/2

## [1.4.3] - 2016-03-31
### added 
[NEW] Floats are now supported for days, hours, and seconds units.  Example ```now-2.5d```, ```now-3.2h```. Any other unit other than days, hours, or seconds that is a float will be converted to an int and floored due to the datetime() module not being able to handle them.