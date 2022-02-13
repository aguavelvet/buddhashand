import csv

from ..input_handler import InputHandler
from ..input_provider import InputProvider

'''
CSVInputProvider.  The class implements the Input Provider interface.

'''
class LineBasedInputProvider(InputProvider):

    def __init__(self, handler: InputHandler, config: map):

        self.handler = handler
        self.config = config

        # note that each input provider defines it's own parameter structure in the configuration json object.
        if self.config['type'].upper() != 'LINE':
            raise ValueError(f"Invalid Type {self.config['type']}for Line Input Provider.")

        self.file = open(self.config['input'],'r',newline='')


    def start (self):
        '''
        start the consumption process.  read in each record and dispatch it to the input handler
        to deal with whatever the processing it needs to do.
        :return:
        '''

        while True:
            line = self.file.readline()
            if not line:
                break

            self.handler.handle({"INPUT": line})


    def done (self):
        '''
        be a good citizen by cleaning up after self.
        :return:
        '''
        try:
            if self.file:
                self.file.close()
        except:
            # not much you can do if we get an exception here...
            pass

