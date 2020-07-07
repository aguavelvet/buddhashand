

class InputProvider:

    def __init__(self,input_handler, man:dict):
        self.handler = input_handler
        self.config = man

    def start (self):
        raise NotImplemented ('Abstract start() method called on the base class... Should not happen')

    def done (self):
        raise NotImplemented ('Abstract done() method called on the base class... Should not happen')
