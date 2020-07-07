

from src.transformer import Transform

'''
Identity transformer. 
'''
class IdentityTransformer(Transform):

    def __init__(self, cfg:map):
        pass

    def transform (self, rec: dict) -> dict:
        return rec