
'''
this file contains a set of functtions that are available in the simple expression parser.
for additional info, see: https://pypi.org/project/simpleeval/
'''
import json
import numpy as np


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
    "jsonify" : jsonify
}

s_op_registry = {

}
