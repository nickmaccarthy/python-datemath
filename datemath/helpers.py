'''
A basic utility module for parsing math like strings relating to dates

This is inspired by Date Math features in elasticsearch and aims to replicate the same functionality for python.

DateMath (datemath or dm) suppor addition, subtraction and rounding at various granularities of "units" (a map of units to their shorthand is below for reference).
Expressions can be chanied together and are read left to right.  '+' and '-' denote addition and subtraction while '/' denotes 'round', in this case is a 'round down' or floor.
Round requires a unit (/d), while addition and subtraction require an integer value and a unit (+1d).  Whitespace is not allowed in the expression.  Absolute datetimes with datemath 
can be made as well, with the datetime and datemath expressions delinated by '||' - example '2015-01-01||+1d' == '2015-01-02'


Maps:

y or Y      =   'year'
M           =   'month'
m           =   'minute'
d or D      =   'day'
w           =   'week'
h or H      =   'hour'
s or S      =   'second'

Examples:

Assuming our datetime is currently: '2016-01-01T00:00:00-00:00'

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

'''

import arrow
import re

debug = False 

class DateMathException(BaseException):
    pass 


def unitMap(c):
    ''' 
        maps our units ( 'd', 'y', 'M', etc ) to shorthands required for arrow
    '''

    if c == 'y' or c == 'Y':
        return 'years'
    elif c == 'M':
        return 'months'
    elif c == 'm':
        return 'minutes'
    elif c == 'd' or c == 'D':
        return 'days'
    elif c == 'w' or c == 'W': 
        return 'weeks'
    elif c == 'h' or c == 'H':
        return 'hours'
    elif c == 's' or c == 'S':
        return 'seconds'
    else:
        raise DateMathException("Not a valid offset: {0}".format(c))

def as_datetime(expression, now, tz='UTC'):
    return parse(expression, now, tz)

def parse(expression, now=None, tz='UTC', type=None):
    if now is None:
        now = arrow.utcnow()

    if debug: print("Orig Expression: {0}".format(expression))

    math = ''
    time = ''

    if 'UTC' not in tz:
        if debug: print("will now convert tz to {0}".format(tz))
        now = now.to(tz)

    if expression == 'now':
        if debug: print("Now, no dm: {0}".format(now))
        if type:
            return getattr(now, type)
        else:
            return now
    elif expression.startswith('now'):
        ''' parse our standard "now+1d" kind of queries '''
        math = expression[3:]
        time = now
        if debug: print('now expression: {0}'.format(now))
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
            math = ''
            time = parseTime(expression, tz)

    if not math or math == '':
        rettime = time

    rettime = evaluate(math, time, tz)
    if type:
        return getattr(rettime, type)
    else:
        return rettime
        


def parseTime(timestamp, tz='UTC'):
    #if timestamp and len(timestamp) >= 4 and (timestamp >= 0 or timestamp < 0): 
    if timestamp and len(timestamp) >= 4: 
        return arrow.get(timestamp)
        
    
def roundDate(now, unit, tz='UTC'):
    now = now.floor(unit)
    if debug: print("roundDate Now: {0}".format(now))
    return now

def calculate(now, offsetval, unit):
    try:
        now = now.replace(**{unit: offsetval})
        return now
    except:
        raise DateMathException('Unable to calculate date: now: {0}, offsetvalue: {1}, unit: {2}'.format(now,offsetval,unit))

def evaluate(expression, now, timeZone='UTC'):
    if debug: print('Expression: {0}'.format(expression))
    if debug: print('Now: {0}'.format(now))
    val = 0
    for i, c in enumerate(expression):
        char = expression[i]

        if i >= len(expression):
            raise('Truncated datemath: {0}'.format(expression))

        if '/' in char:
            # then we need to round up
            next = str(expression[i+1])

            roundUp = True            
            now = roundDate(now, unitMap(next).rstrip('s'), timeZone)

        elif char == '+' or char == '-':
            if i >= len(expression):
                raise DateMathException('Truncated datemath: {0}'.format(expression))

            val = 0

            try:
                m = re.match('(\d+)[\w+-/]', expression[i+1:])
                num = m.group(1)
                val = val * 10 + int(num, 10)
                i = i + len(num)
            except Exception as e:
                raise DateMathException("Invalid numerical datematch: What I got was - match: {0}, expression: {1}, error: {2}".format(expression[i+1:], expression, e)) 
    
            if char == '+':
                val = int(val)
            else:
                val = int(-val)
            
        elif re.match('[a-zA-Z]+', char):
            now = calculate(now, val, unitMap(char))
        
        i = i+1
    if debug: print("Fin: {0}".format(now))
    if debug: print('\n\n')
    return now



if __name__ == "__main__":
    if debug: print('NOW: {0}'.format(arrow.utcnow()))
    if debug: print('\n\n')
    parse('now-1h')
    parse('now+12h')
    parse('now+1h')
    parse('now+1h+1m')
    parse('now+1h/d')
    parse('now-2d/d')
    parse('2012-01-01||+1M/d')
    parse('now+1w/w')
    parse('+1d/d')
    parse('/h')
    parse('/d')
    parse('2014-11-18||+1M/M')
    parse('2014-11-18||+1M/M+1h')
    parse('2014-11-18||/w')
    parse('2014-11-18||/y')
    parse('2014-11-18||+1M-1m')
    print(parse('now/d+7d+12h'))
    print(parse('now', tz='US/Pacific'))
    print(type(parse('now-10m', type='datetime')))
    print(type(parse('now', type='datetime')))
