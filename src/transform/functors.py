
'''
this file contains a set of functtions that are available in the simple expression parser.
for additional info, see: https://pypi.org/project/simpleeval/
'''
import json
import random

import numpy as np
from  ..misc.memory_cache import MemoryCache
import json
from jsonpath_ng import jsonpath, parse

def get_fn_registry():
    return s_fn_registry


def get_op_registry():
    return s_op_registry


# ------------------------------------------------functions ------------------------------------------------------------
def unity(x):
    '''
        basic function that takes a parameter and returns it.  Mainly useful for testing.
    '''
    return x


def inverse(x):
    '''
        return 1/x.
    '''
    return 'nan' if x == 0 else 1/ x


def mult(x,y):
    '''
    multiply two numbers.
    '''
    return (float)(float(x)*float(y))


def var95(pnl):
    '''
    calculate VaR95 of the given pln vector.
    :param pnl:  PnL vector.
    :return:  VaR95
    '''
    slist    = sorted(pnl)
    percent = np.percentile(slist,95)

    return percent


def PI():
    return 3.141529


def xpaths(rec, path):
    expr = parse(path)

    if "_meta_state" in path:
        rec = rec.replace("_meta.state", "_meta_state")
    match = expr.find (json.loads(rec))

    return '' if len(match) == 0 else match[0].value


def volatility(pnl, annualize=True):

    vol = np.std(pnl)
    if annualize:
        vol = vol*np.sqrt(252)

    return vol


def jsonify(field_names,  rec: map):

    # ['scheddate', 'descr', wostatus'...]
    jsn = {}
    fields = field_names.split(',')
    for f in fields:
        f = f.strip()
        jsn[f] = str(rec[f]).strip()

    return json.dumps(jsn)


def namespace_lookup(ns,key, dflt=''):
    val = MemoryCache.get_value(ns,key)
    return  dflt if val is None else val


def default (val, dflt):
    return dflt if val is None or val == '' else dflt


def assert_not_null (fname, val):
    if val is None:
        raise ValueError(f'The field {fname} was found to be null.')
    return val


def randrange (start: int, end: int):
    return random.randrange(start,end)


def randelem(elements: str):

    elems = elements.split(',')

    return elements[random.randrange(0, len(elems))]


def randdob(startY, endY):

    y = random.randrange(startY, endY)
    m = random.randrange(1, 12)

    if m in [1,3,5,7,8,10,12]:
        M = 31
    elif m in [4,6,9,11]:
        M = 30
    else:
        M = 29 if (y % 4 == 0 or  y%100) else 28

    d = random.randrange(1,M)

    return f"{y}-{m}-{d}"


# ------------------------------------------------functions ------------------------------------------------------------


# ------------------------------------------------operators ------------------------------------------------------------
#  We have not defined our own operator yet.  But we can easily do that. Here is an example how to add an operator.


def at_op(x, y):
    return x + '@' + y


s_op_registry = {
    # example registry.
    '@': at_op
}

# ------------------------------------------------operators ------------------------------------------------------------


s_fn_registry = {
    "unity": unity,
    "inverse": inverse,
    "mult": mult,
    "var95": var95,
    "volatility" : volatility,
    "jsonify" : jsonify,
    "namespace_lookup" : namespace_lookup,
    "default" : default,
    "assert_not_null" : assert_not_null,
    "xpaths" : xpaths,
    "randrange" : randrange,
    "randelem" : randelem,
    "randdob"  : randdob
}

