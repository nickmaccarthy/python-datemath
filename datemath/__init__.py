from .helpers import parse, DateMathException

def dm(expr, **kwargs):
    ''' does our datemath and returns an arrow object '''
    return parse(expr, **kwargs)

def datemath(expr, **kwargs):
    ''' does our datemath and returns a datetime object '''
    return parse(expr, **kwargs).datetime
