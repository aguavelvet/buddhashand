

# ----------------------------------------------------------------------------------------------------------------------
# abstract class.
class InputHandler(object):

    def handle (self, rec:map):
        raise NotImplementedError('InputHandler must implement the handle method.')

    def done(self):
        raise NotImplementedError('InputHandler must implement done  method.')
