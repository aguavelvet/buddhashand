import csv

from ..input_handler import InputHandler


'''
CSVInputProvider.  The class implements the Input Provider interface.

'''
class CSVInputProvider:

    def __init__(self, handler: InputHandler, config: map):

        self.handler = handler
        self.config = config

        # note that each input provider defines it's own parameter structure in the
        # configuration json object.
        if self.config['type'].upper() != 'CSV':
            raise ValueError(f"Invalid Type {self.config['type']}for CSV Input Provider.")

        self.reader = csv.DictReader(open(self.config['input'],'r',newline=''))
        self.header = None


    def start (self):
        '''
        start the consumption process.  read in each record and dispatch it to the input handler
        to deal with whatever the processing it needs to do.
        :return:
        '''

        for row in self.reader:
            self.handler.handle (row)


    def done (self):
        '''
        be a good citizen by cleaning up after self.
        :return:
        '''
        try:
            if self.reader is not None:
                del self.reader
        except:
            # not much you can do if we get an exception here...
            pass

