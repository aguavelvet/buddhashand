
import json
from json import JSONEncoder
from genson import SchemaBuilder
from src.output_handler import OutputHandler


class UniqueCSVOutputHandler(OutputHandler):

    class EmptyEncoder(json.JSONEncoder):
        def empty(self, o):
            o = '' if (isinstance(o, str) or isinstance(o, int) or o is None) else o
            return self._encode(o)

        def _encode(self, obj):
            if isinstance(obj, dict):
                return {k: self.empty(v) for k,v in obj.items()}
            elif isinstance(obj, list):
                return [self.empty(o)  for o in obj]
            else:
                return obj

        def encode(self, obj):
            return super(UniqueCSVOutputHandler.EmptyEncoder, self).encode(self._encode(obj))

    def __init__(self, cfg):
        self.config = cfg
        self.writer = None
        self.cache = {}
        self.unique_field = cfg['unique_field'] if 'unique_field' in cfg else None
        if cfg['type'].upper() != 'UNIQUE_CSV':
            raise ValueError ("Invalid output type.  Expecting UNIQUE_CSV!.")

    def stripJson (fld):
        if isinstance(fld, dict):
            val = json.dumps(fld, cls=UniqueCSVOutputHandler.EmptyEncoder)
            return val

        return str(fld)

    def toschema (fld):

        if isinstance(fld, dict):
            builder = SchemaBuilder()
            builder.add_object (fld)
            return builder.to_json()

        return str(fld)

    def handle(self, rec: map):

        if not self.writer:
            # if this is the first call, create a output file pointer and write the header.
            outfile = self.config['output']
            self.writer = open(outfile, 'w+')

            hdr = ','.join([x for x in list(map(lambda x: x[0], rec.items()))])
            self.writer.write(hdr)
            self.writer.write('\n')

        vals = list(map (lambda x: x[1], rec.items()))
        row  = ','.join([UniqueCSVOutputHandler.toschema(x) for x in vals])

        if row.__hash__() not in self.cache:
            self.cache[row.__hash__()] = row

    def done(self):
        if self.writer:
            for row in self.cache.values():
                self.writer.write(row)
                self.writer.write('\n')

            try:
                self.writer.flush()
                self.writer.close()
                del self.writer
            except:
                pass
