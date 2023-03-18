import csv

import json
import random

from ..input_handler import InputHandler
from ..input_provider import InputProvider

class TemplateListInputProvider(InputProvider):
    '''
    RangeInputProvider.  The class implements the Input Provider interface.
    This input provider injects a set of records specified by the range.

    '''

    def __init__(self, handler: InputHandler, config: map):

        self.handler = handler
        self.config = config

        self.generate_id = self.config["generate_id"] if "generate_id" in self.config else False

        # note that each input provider defines it's own parameter structure in the configuration json object.
        if self.config['type'].upper() != 'TEMPLATE_LIST':
            raise ValueError(f"Invalid Type {self.config['type']}for Template List  Input Provider.")

        with open (self.config['file'], 'r') as file:
            self.template = json.loads(file.read())


    def start(self):
        '''
        start the consumption process.  read in each record and dispatch it to the input handler
        to deal with whatever the processing it needs to do.
        :return:
        '''

        length = len(self.template)
        for i in range (self.config['range']['start'], self.config['range']['end']):

            x = random.randrange(0, length)
            input = self.template[x].copy()

            if self.generate_id:
                input["_id"] = i

            rec = {"INPUT": input, "COUNTER" : i }
            self.handler.handle(rec)

    def done(self):
        pass
