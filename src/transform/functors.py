
'''
this file contains a set of functtions that are available in the simple expression parser.
for additional info, see: https://pypi.org/project/simpleeval/
'''
import os
import random
import openai
import requests

import numpy as np
from  ..misc.memory_cache import MemoryCache
import json
from jsonpath_ng import jsonpath, parse


def get_fn_registry():
    return s_fn_registry


def get_op_registry():
    return s_op_registry


def get_infa_session():
    return s_session

def set_infa_session(session):
    s_session = session


openai.api_key = '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'

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
    return random.randrange(start, end)


def randelem(elements: str):

    elems = elements.split(',')
    result = elems[random.randrange(0, len(elems))]
    return result.strip();

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

def chatgpt (prompt):
    response = openai.Completion.create(model="text-davinci-003",
                                        prompt=prompt, temperature=0,
                                        max_tokens=7)
    return response

def geocode(addy):
    URL = "http://maps.googleapis.com/maps/api/geocode/json"

    # sending get request and saving the response as response object
    r = requests.get(url=URL, params={'address': addy})

    # extracting data in json format
    data = r.json()

    # of the first matching location
    #latitude = data['results'][0]['geometry']['location']['lat']
    #longitude = data['results'][0]['geometry']['location']['lng']
    #formatted_address = data['results'][0]['formatted_address']
    return data


def infa_login(user,password):
    session = get_infa_session()
    if 'sessionId' not in session:
        IICS = 'https://qa-ma.rel.infaqa.com/identity-service/api/v1/Login'
        session = requests.post(IICS,json={"username": user,"password":password},headers={
            "encoding":"UTF-8",
            "Content-Type" : "application/json"
        })
        set_infa_session(session)

    return session

def get_be(be):
    session = infa_login("kirbyprivate","Password@1")

    URL = 'https://internal-a24f3677d852144a28a327da2e2bd70a-1945347265.us-west-2.elb.amazonaws.com/metadata/api/v2/objects/businessEntity/c360.person'
    content = session.json()
    headers = {
        "IDS-SESSION-ID":content['sessionId'],
        "INFA-MDM-CORRELATION-ID": 'correlationId',
        "Content-Type": "application/json"
    }
    # result = requests.get(url=URL, headers=headers)

    return content['sessionId']


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
s_session = {}

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
    "randdob"  : randdob,
    "chatgpt" : chatgpt,
    "geocode" : geocode,
    "get_be" : get_be
}

