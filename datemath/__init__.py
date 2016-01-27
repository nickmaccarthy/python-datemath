from .helpers import parse

def dm(expr, **kwargs):
    return parse(expr, **kwargs)

def datemath(expr, **kwargs):
    return parse(expr, **kwargs).datetime
