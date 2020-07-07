
from ..output_handler import OutputHandler


class CSVOutputHandler(OutputHandler):

    def __init__(self, cfg):
        self.config = cfg
        self.writer = None

        if cfg['type'].upper() != 'CSV':
            raise ValueError ("Invalid output type.  Expecting CSV.")


    def handle(self, rec: map):

        if self.writer is None:
            # if this is the first call, create a output file pointer and write the header.
            outfile = self.config['output']
            self.writer = open(outfile, 'w+')

            hdr = ','.join([x for x in list(map(lambda x: x[0], rec.items()))])
            self.writer.write(hdr)
            self.writer.write('\n')

        vals = list(map (lambda x: x[1], rec.items()))
        row  = ','.join([str(x) for x in vals])

        self.writer.write(row)
        self.writer.write('\n')

    def done(self):
        if self.writer is not None:
            try:
                self.writer.flush()
                self.writer.close()
                del self.writer
            except:
                pass
