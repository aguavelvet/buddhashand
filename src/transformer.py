

# ----------------------------------------------------------------------------------------------------------------------
# abstract class.
# ----------------------------------------------------------------------------------------------------------------------

class Transform(object):

    def transform (self, rec: map):
        raise NotImplementedError('Transformer must implement the transform method. Should never happen.')

