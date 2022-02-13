
from src.transformer import Transform


class IdentityTransformer(Transform):
    '''
         Identity Transformer
    '''

    def __init__(self, cfg:map):
        pass

    def transform (self, rec: dict) -> dict:
        return rec