import json
import decimal
from src.output_handler import OutputHandler

import pymongo


class MongoOutputHandler(OutputHandler):

    def __init__(self, cfg):

        if cfg['type'].upper() != 'MONGODB':
            raise ValueError ("Invalid output type.  Expecting MONGODB.")
        self.batch = []
        self.config = cfg
        self.client = pymongo.MongoClient(f"mongodb://{cfg['host']}:{cfg['port']}/")
        self.database = self.client[cfg['database']]
        self.collection = self.database[cfg['collection']]
        self.batchsize = cfg['batchsize'] if 'batchsize' in cfg else 1


    def handle(self, rec: map):

        self.batch.append(rec)
        if len(self.batch) >= self.batchsize:
            self.collection.insert_many(self.batch)
            self.batch.clear()


    def done(self):
        if self.client:
            if len(self.batch) > 0:
                self.collection.insert_many(self.batch)
                self.batch.clear()

            self.client.close()
