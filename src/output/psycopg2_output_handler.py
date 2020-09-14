
import re
import psycopg2
from ..output_handler import OutputHandler




class Psycopg2OutputHandler(OutputHandler):

    def __init__(self, cfg):

        if cfg['type'].upper() != 'POSTGRES':
            raise ValueError ("Invalid output type.  Expecting POSTGRES.")

        self.config = cfg
        self.batch = []
        self.count = 0
        self.batchsize = 1

        if 'batchsize' in self.config:
            self.batchsize = self.config['batchsize']
            assert self.batchsize > 0

        self.sql  = self.config['sql']
        self.conn = psycopg2.connect(user=cfg['user'], password=cfg['pswd'],
                                     host=cfg['host'], port=cfg['port'], database=cfg['database'])
        self.cursor = None

        self.keys = Psycopg2OutputHandler._get_keys(self.sql)


    def _get_keys(sql:str):
        if 'INSERT' not in sql.upper():
            raise ValueError (f'Not an insert statement [{sql}].')

        keys  = []
        subs  = re.search("\((.+?)\)",sql).group(0)[1:-1]
        parts = subs.split(',')
        for p in parts:
            keys.append(p.strip())
        return keys


    def handle(self, rec: map):

        if self.cursor is None:
            self.cursor = self.conn.cursor()

        if self.batchsize == 1:
            vals = [rec[x] for x in self.keys]
            self.cursor.execute(self.sql, tuple(vals))
            self.conn.commit()
        else:
            self.count += 1

            self.batch.append (tuple ([rec[x] for x in self.keys]))
            if self.batchsize == self.count:
                self.cursor.executemany(self.sql, self.batch)
                self.conn.commit()

                self.count = 0
                self.batch.clear()
                print()

    def done(self):

        if self.cursor is not None:
            try:
                if len(self.batch) > 0:
                    self.cursor.executemany(self.sql, self.batch)
                self.conn.commit()

                self.conn.close()

            except:
                pass
