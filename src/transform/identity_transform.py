
from src.transformer import Transform
from src.transform.functors import randrange

class IdentityTransformer(Transform):
    '''
         Identity Transformer
    '''

    def __init__(self, cfg:map):
        pass

    def transform (self, rec: dict) -> dict:
        input = rec['INPUT'] if ('INPUT' in rec) else rec

        # input["handlerData"]["changeList"] = str(randrange(0, 200000))
        # input["changeListId"] = str(randrange(0,200000))

        return input


    def transform_orig (self, rec: dict) -> dict:
        return rec['INPUT'] if ('INPUT' in rec) else rec
