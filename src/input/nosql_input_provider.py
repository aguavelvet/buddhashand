

from ..input_handler import InputHandler

class NOSQLInputProvider:

    def __init__(self, handler: InputHandler, config: map):

        self.handler = handler
        self.config = config




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

