
'''
this file contains a set of functtions that are available in the simple expression parser.
for additional info, see: https://pypi.org/project/simpleeval/
'''


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
        return 1/x
    '''
    return 'nan' if x == 0 else 1/ x

def mult(x,y):

    X = float(x) if type(x) == str else x
    Y = float(y) if type(y) == str else y

    return (float)(X*Y)

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
    "mult": mult
}

s_op_registry = {

}
