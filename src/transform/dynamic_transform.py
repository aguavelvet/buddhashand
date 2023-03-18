import os
from src.transform.reference_transform import ReferenceTransformer
from src.transform.functors import get_fn_registry
from simpleeval import SimpleEval


class DynamicTransformer(ReferenceTransformer):

    def __init__(self, cfg:map):
        super(DynamicTransformer,self).__init__(cfg)

    def transform (self, irec:dict) -> dict:
        self.template = irec['transform']
        irec['COUNTER'] = 0
        irec['OUTPUT'] = super().transform(irec)
        return irec['OUTPUT']


