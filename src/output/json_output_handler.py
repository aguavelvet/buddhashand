from ..output_handler import OutputHandler

class JsonOutputHandler(OutputHandler):

    def __init__(self, cfg):
        self.config = cfg


    def handle(self, rec: map):
        pass

    def done(self):
        pass
