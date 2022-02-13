import csv

from ..input_handler import InputHandler
from ..input_provider import InputProvider

class RangeInputProvider(InputProvider):
    '''
    RangeInputProvider.  The class implements the Input Provider interface.
    This input provider injects a set of records specified by the range.

    '''

    def __init__(self, handler: InputHandler, config: map):

        self.handler = handler
        self.config = config

        # note that each input provider defines it's own parameter structure in the configuration json object.
        if self.config['type'].upper() != 'RANGE':
            raise ValueError(f"Invalid Type {self.config['type']}for Range Input Provider.")

    def start(self):
        '''
        start the consumption process.  read in each record and dispatch it to the input handler
        to deal with whatever the processing it needs to do.
        :return:
        '''

        for i in range (self.config['range']['start'], self.config['range']['end']):

            self.handler.handle({
                "INPUT": self.config['record'],
                "COUNTER" : i
            })

    def done(self):
        pass
