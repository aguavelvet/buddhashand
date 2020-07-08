import pymongo
import json

from ..input_handler import InputHandler
from ..input_provider import InputProvider


class MongoDBInputProvider(InputProvider):

    def __init__(self, handler: InputHandler, config: map):

        self.handler = handler
        self.config = config
        self.client = pymongo.MongoClient(f'mongodb://{config["host"]}:{config["port"]}')
        self.mongodb = self.client[config['database']]


    def start (self):
        '''
        start the consumption process.  read in each record and dispatch it to the input handler
        to deal with whatever the processing it needs to do.
        Please refer to:
        https://docs.mongodb.com/manual/reference/method/
        https://docs.mongodb.com/manual/reference/method/js-collection/
        :return:
        '''

        coll   = self.config['collection']
        query  = json.loads(self.config['query'])
        filtstr = self.config['filter']
        filter = {} if filtstr == "" else json.loads(filtstr)

        for doc in self.mongodb[coll].find(query,filter):
            print (doc)
            self.handler.handle (doc)


    def done (self):
        '''
        be a good citizen by cleaning up after self.
        :return:
        '''
        try:
            if self.client is not None:
                self.client.close()
        except:
            # not much you can do if we get an exception here...
            pass

