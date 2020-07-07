import os
from .input_handler import InputHandler
from .output_handler import OutputHandler
from src.conf.factory import Factory

import logging

logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
class Buddhashand(InputHandler):

    def __init__(self, man: map):
        self.man = man
        self.iprovider = Factory.create_input_provider(self, man['input'])
        self.transform = Factory.create_transformer(man['transform'])
        self.ohandler  = Factory.create_output_handler(man['output'])
        self.env = os.environ.copy()

        self.row_count = 0
        self.err_count = 0
        self.filtered  = 0


    def handle(self, irec: map):
        '''
        handle the input record. Dispatch to the transformer then to the output handler.
        Note that what comes back from the transformer may be different from the input record, including
        returning map reduced values or map increased values.

        :param irec: input record.
        :return:
        '''

        self.row_count +=1

        # set up some environment variables that can be accessed by the down stream handlers
        self.env['INPUT'] = irec
        self.env['RECORD'] = irec

        print (irec)

        try:
            # do not allow errors to propagate.  We want to continue on best effort basis.
            orec = self.transform.transform(irec)
            if orec is not None:
                self.filtered += 1
                self.ohandler.handle(orec)
        except Exception as ex:
            self.err_count += 1
            logger.error(str(ex))


    def process(self):
        '''
        process the pipe line.  start will for all intent and purpose hand over the driving process
        over to the input handler.  It then will dispatch the input record to the Input Handler (which is implemented
        here, but doesn't have to).  The input handler will dispatch to the transformer and finally to the
        '''

        self.iprovider.start()
        self.iprovider.done()
        self.ohandler.done()

        print (f'Processed {self.row_count} rows.  Filtered {self.filtered} rows with {self.err_count} errors.')

    def done  (self):
        '''
        be a good citizen.  clean up after yourself... Note that if we get an exception here,
        there's not much we can do aside from logging it.
        :return:
        '''
        try:
            self.iprovider.done()
        except Exception as ex:
            logger.warning(f'received exception {str(ex)} while cleaning up...')

        try:
            self.transform.done()
        except Exception as ex:
            logger.warning(f'received exception {str(ex)} while cleaning up...')

        try:
            self.ohandler.done()
        except Exception as ex:
            logger.warning(f'received exception {str(ex)} while cleaning up...')
