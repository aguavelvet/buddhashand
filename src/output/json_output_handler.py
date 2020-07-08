import json
import decimal
from ..output_handler import OutputHandler


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


class JsonOutputHandler(OutputHandler):

    def __init__(self, cfg):

        if cfg['type'].upper() != 'JSON':
            raise ValueError ("Invalid output type.  Expecting JSON.")

        self.config = cfg
        self.writer = None

    def handle(self, rec: map):

        if self.writer is None:
            # if this is the first call, create a output file pointer and write the header.
            outfile = self.config['output']
            self.writer = open(outfile, 'w+')
            self.writer.write('[\n')
        else:
            self.writer.write(',\n')

        dump = json.dumps(rec, indent=4, cls=DecimalEncoder)
        self.writer.write(dump)

    def done(self):
        if self.writer is not None:
            try:
                self.writer.write('\n]\n')
                self.writer.flush()
                self.writer.close()
                del self.writer
            except:
                pass
