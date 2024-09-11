from __future__ import annotations

import os
import re
from typing import TypedDict, cast

import arrow
from arrow import Arrow

debug = True if os.environ.get('DATEMATH_DEBUG') else False 

class DateMathException(Exception):
    pass 

def unitMap(c: str) -> str:
    ''' 
        maps our units ( 'd', 'y', 'M', etc ) to shorthands required for arrow
    '''

    if c == 'y' or c == 'Y' or c.lower() == 'years' or c.lower() == 'year':
        return 'years'
    elif c == 'M' or c.lower() == 'months' or c.lower() == 'month':
        return 'months'
    elif c == 'm' or c.lower() == 'minute' or c.lower() == 'minute':
        return 'minutes'
    elif c == 'd' or c == 'D' or c.lower() == 'days' or c.lower() == 'day':
        return 'days'
    elif c == 'w' or c == 'W' or c.lower() == 'weeks' or c.lower() == 'week': 
        return 'weeks'
    elif c == 'h' or c == 'H' or c.lower() == 'hours' or c.lower() == 'hour':
        return 'hours'
    elif c == 's' or c == 'S' or c.lower() == 'seconds' or c.lower() == 'second':
        return 'seconds'
    elif c.lower() == 'n' or c.lower() == 'now':
        raise DateMathException("""Timeunit: "{0}" is not valid.  If you are trying to specify 'now' after timestamp (i.e. 2016-01-01||now/d) that is not valid.  Please try 2016-01-01||/d instead""".format(c))
    else:
        raise DateMathException("Not a valid timeunit: {0}".format(c))

class ParseParams(TypedDict, total=False):
    now: Arrow | None
    tz: str
    type: str | None
    roundDown: bool

def parse(expression: str | int, now: Arrow | None = None, tz: str = 'UTC', type: str | None = None, roundDown: bool = True) -> Arrow:
    '''
        the main meat and potatoes of this this whole thing
        takes our datemath expression and does our date math
        :param expression - the datemath expression
        :param now - what time is now; when will now be then?  soon
        :param type - if we are dealing with a arrow or datetime object
        :param roundDown - wether or not we should round up or round down on this.  default is roundDown=True, which means if it was 12:00:00, `/d` would be '00:00:00', and with roundDown=False, `/d` would be '29:59:59'
    '''
    if debug: print("parse() - starting for expression: {}".format(expression))
    if now is None:
        if debug: print("parse() - Now is None, setting now to utcnow()")
        now = arrow.utcnow()

    if debug: print("parse() - Orig Expression: {0}".format(expression))

    math = ''
    time = None

    if 'UTC' not in tz:
        if debug: print("parse() - will now convert tz to {0}".format(tz))
        now = now.to(tz)

    expression = str(expression)
    if expression == 'now':
        if debug: print("parse() - Now, no dm: {0}".format(now))
        if type:
            return cast(Arrow, getattr(now, type))
        else:
            return now
    elif re.match(r'\d{10,}', expression):
        if debug: print('parse() - found an epoch timestamp')
        if len(expression) == 13:
            raise DateMathException('Unable to parse epoch timestamps in millis, please convert to the nearest second to continue - i.e. 1451610061 / 1000')
        ts = arrow.get(int(expression))
        ts = ts.replace(tzinfo=tz)
        return ts
    elif expression.startswith('now'):
        ''' parse our standard "now+1d" kind of queries '''
        math = expression[3:]
        time = now
        if debug: print('parse() - now expression: {0}'.format(now))
    else:
        ''' parse out datemath with date, ex "2015-10-20||+1d"  '''
        if '||' in expression:
            timestamp, math = expression.split('||')
            time = parseTime(timestamp, tz)
        elif expression.startswith(('+', '-', '/')):
            '''
            this catches expressions that don't start with 'now' but we are assume are 'now', such as 
            '+1h', '-2/w', '/1d', '+2h-2m', etc
            '''
            math = expression
            time = now
        else:
            if debug: print('parse() - Found and expression that will hit the catchall')
            math = ''
            time = parseTime(expression, tz)

    if not math or math == '':
        rettime = time

    rettime = evaluate(math, time, tz, roundDown)

    if type:
        return cast(Arrow, getattr(rettime, type))
    else:
        return rettime
        
def parseTime(timestamp: str, timezone: str = 'UTC') -> Arrow:
    '''
        parses a datetime string and returns and arrow object
    '''
    if timestamp and len(timestamp) >= 4: 
        ts = arrow.get(timestamp)
        if debug: print("parseTime() - ts = {} :: vars :: {}".format(ts, vars(ts)))
        if debug: print("parseTime() - ts timezone = {}".format(ts.tzinfo))
        if debug: print("parseTime() - tzinfo type = {}".format(type(ts.tzinfo)))
        if debug: print("parseTime() - timezone that came in = {}".format(timezone))

        if ts.tzinfo:
            import dateutil.tz
            if isinstance(ts.tzinfo, dateutil.tz.tz.tzoffset):
            # this means our TZ probably came in via our datetime string
            # then lets set our tz to whatever tzoffset is
                ts = ts.replace(tzinfo=ts.tzinfo)
            elif isinstance(ts.tzinfo, dateutil.tz.tz.tzutc):
            # otherwise if we are utc, then lets just set it to be as such
                ts = ts.replace(tzinfo=timezone)
        else: 
            # otherwise lets just ensure its set to whatever timezone came in
            ts = ts.replace(tzinfo=timezone)
        
        return ts
    else:
        if debug: print('parseTime() - Doesnt look like we have a valid timestamp, raise an exception.  timestamp={}'.format(timestamp))
        raise DateMathException('Valid length timestamp not provide, you gave me a timestamp of "{}", but I need something that has a len() >= 4'.format(timestamp))
          
def roundDate(now: Arrow, unit: str, tz: str = 'UTC', roundDown: bool = True) -> Arrow:
    '''
        rounds our date object
    '''
    if roundDown:
        now = now.floor(unit)  # type: ignore[arg-type]
    else:
        now = now.ceil(unit) # type: ignore[arg-type]
    if debug: print("roundDate() Now: {0}".format(now))
    return now

def calculate(now: Arrow, offsetval: float, unit: str) -> Arrow:
    '''
        calculates our dateobject using arrows replace method
        see unitMap() for more details
    ''' 
    if unit not in ('days','hours','seconds'):
        offsetval = int(offsetval)
    try:
        now = now.shift(**{unit: offsetval})
        if debug: print("calculate() called:  now: {}, offsetval: {}, offsetval-type: {}, unit: {}".format(now, offsetval, type(offsetval), unit))
        return now
    except Exception as e:
        raise DateMathException('Unable to calculate date: now: {0}, offsetvalue: {1}, unit: {2} - reason: {3}'.format(now,offsetval,unit,e))

def evaluate(expression: str, now: Arrow, timeZone: str = 'UTC', roundDown: bool = True) -> Arrow:
    '''
        evaluates our datemath style expression
    '''
    if debug: print('evaluate() - Expression: {0}'.format(expression))
    if debug: print('evaluate() - Now: {0}'.format(now))
    val = float(0)
    i = 0
    while i < len(expression):
        char = expression[i]

        if '/' in char:
            # then we need to round
            next = str(expression[i+1])
            i += 1
            now = roundDate(now, unitMap(next).rstrip('s'), timeZone, roundDown)

        elif char == '+' or char == '-':
            val = 0

            try:
                m = re.match(r'(\d*[.]?\d+)[\w+-/]', expression[i+1:])
                if m:
                    num = m.group(1)
                    val = val * 10 + float(num)
                    i = i + len(num)
                else:
                    raise DateMathException('''Unable to determine a proper time qualifier.  Do you have a proper numerical number followed by a valid time unit? i.e. '+1d', '-3d/d', etc.''')
            except Exception as e:
                raise DateMathException("Invalid datematch: What I got was - re.match: {0}, expression: {1}, error: {2}".format(expression[i+1:], expression, e)) 
    
            if char == '+':
                val = float(val)
            else:
                val = float(-val)
        elif re.match(r'[a-zA-Z]+', char):
            now = calculate(now, val, unitMap(char))
        else:
            raise DateMathException(''''{}' is not a valid timeunit for expression: '{}' '''.format(char, expression))
        
        i += 1
    if debug: print("evaluate() - Finished: {0}".format(now))
    if debug: print('\n\n')
    return now

if __name__ == "__main__":
    if debug: print('NOW: {0}'.format(arrow.utcnow()))
    if debug: print('\n\n')
    #parse('now-1h')
    #parse('now+12h')
    #parse('now+1h')
    #parse('now+1h+1m')
    #parse('now+1h/d')
    #parse('now-2d/d')
    #parse('2012-01-01||+1M/d')
    #parse('now+1w/w')
    #parse('+1d/d')
    #parse('/h')
    #parse('/d')
    #parse('2014-11-18||+1M/M')
    #parse('2014-11-18||+1M/M+1h')
    #parse('2014-11-18||/w')
    #parse('2014-11-18||/y')
    #parse('2014-11-18||+1M-1m')
    #print(parse('now/d+7d+12h'))
    #print(parse('now', tz='US/Pacific'))
    #print(type(parse('now-10m', type='datetime')))
    #print(type(parse('now', type='datetime')))
    #print(parse('now-2.5h'))
    #print(parse('2016-01-01||-3.2h'))
    #print(parse('now', tz='US/Pacific'))
    #print(parse('2017-09-22T10:20:00', tz='US/Eastern'))
