import json
import decimal
from src.output_handler import OutputHandler

import pymongo


class MongoOutputHandler(OutputHandler):

    def __init__(self, cfg):

        if cfg['type'].upper() != 'MONGODB':
            raise ValueError ("Invalid output type.  Expecting MONGODB.")

        self.config = cfg
        self.client = pymongo.MongoClient(f"mongodb://{cfg['host']}:{cfg['port']}/")
        self.database = self.client[cfg['database']]
        self.collection = self.database[cfg['collection']]

    def handle(self, rec: map):

        if self.collection is not None:
            self.collection.insert_one(rec)

    def done(self):
        if self.client:
            self.client.close()
