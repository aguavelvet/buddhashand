import os
import json
import pymongo
import random

host = 'localhost'
port = 27017
dbname = 'dbqt'


def getPnL ():
    pnl = []
    for i in range(252):
        pnl.append(random.random())
    return pnl

client = pymongo.MongoClient(f'mongodb://{host}:{port}')

# if the database exists, drop it before recreating it.
dbs = client.list_database_names()
if dbname in dbs:
    client.drop_database(dbname)

dbqt  = client[dbname]
instrument = dbqt['instrument']

instr = []
tickers = ["AAPL", "AC", "AMZN", "BB", "BCE", "BNS", "ENB", "FB", "MSFT", "GOOGL", "T", "TD", "TSLA", "WMT", "SHOP"]
for t in tickers:
    instr.append ({"Ticker" : t, "PnL" : getPnL ()})

ids = instrument.insert_many(instr)
print (ids.inserted_ids)
