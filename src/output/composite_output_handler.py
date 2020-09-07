
from ..output_handler import OutputHandler


class CompositeOutputHandler(OutputHandler):

    def __init__(self, cfg):
        self.config = cfg
        self.writer = None
        self.outmap = {}

        if cfg['type'].upper() != 'COMPOSITE':
            raise ValueError ("Invalid output type.  Expecting CSV.")

        if 'namespaces' not in cfg:
            raise ValueError ("Composite Output Handler requires namesspaces configuration.")

        namespaces = cfg['namespaces']

        from src.conf.factory import Factory
        for key,ns in namespaces.items():
            self.outmap[key] = Factory.create_output_handler(ns)

    def iterable(self, obj):
        '''Determine if the object can be iterated.'''
        try:
            iter(obj)
        except Exception:
            return False
        else:
            return True

    def handle(self, rec: map):
        '''
        handle the incoming record.  The record is expected to be a map of namespace:record
        :param rec:  namespace : record.  If the record is iterable, the object is iterated into the output handler.
        :return:
        '''

        for ns,ns_rec in rec.items():
            if ns not in self.outmap:
                raise ValueError(f"Composite Output handler encountered an unknown namespace {ns}.  Critical Error.")

            handler = self.outmap[ns]
            handler.handle(ns_rec)


    def done(self):

        for key,handler in self.outmap.items():
            handler.done()
