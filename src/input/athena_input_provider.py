
import os
from pyathenajdbc import connect

from ..input_handler import InputHandler
from ..input_provider import InputProvider


class AthenaInputProvider(InputProvider):

    def __init__(self, handler: InputHandler, config: map):

        self.handler = handler
        self.config = config
        self.conn   = connect(UID=config['aws_access_key_id'],
                              PWD=config['aws_secret_access_key'],
                              Schema=config['schema'],
                              S3OutputLocation=config['s3_out_dir'],
                              AwsRegion=config['region_name'])

        #self.conn = connect(aws_access_key_id=config['aws_access_key_id'],
        #                    aws_secret_access_key=config['aws_secret_access_key'],
        #                    s3_staging_dir=config['s3_staging_dir'], region_name=config['region_name'])


    def start (self):
        '''
        start the consumption process.  read in each record from mysql and dispatch it to the input handler
        to deal with whatever the processing it needs to do.
        :return:
        '''

        c = self.conn.cursor()

        c.execute(self.config['sql'])

        hdr = [h[0] for h in c.description]
        rs = c.fetchall()

        for r in rs:
            row = dict(zip(hdr, r))
            self.handler.handle (row)


    def done (self):
        '''
        be a good citizen by cleaning up after self.
        :return:
        '''
        try:
            if self.conn  is not None:
                self.conn.close()
        except:
            # not much you can do if we get an exception here...
            pass

