from ..input_provider import InputProvider
from ..output_handler import OutputHandler

from src.input.csv_input_provider import CSVInputProvider
from src.input.http_input_provider import HttpInputProvider
from src.input.mongodb_input_provider import MongoDBInputProvider
from src.input.mysql_input_provider import MYSQLInputProvider
from src.input.psycopg2_input_provider import Psycopg2InputProvider
from src.input.athena_input_provider import AthenaInputProvider
from src.input.linebased_input_provider import LineBasedInputProvider
from src.input.range_input_provider import RangeInputProvider
from src.input.template_list_input_provider import TemplateListInputProvider

from src.output.csv_output_handler import CSVOutputHandler
from src.output.json_output_handler import JsonOutputHandler
from src.output.csv_unique_output_handler import UniqueCSVOutputHandler
from src.output.composite_output_handler import CompositeOutputHandler
from src.output.psycopg2_output_handler import Psycopg2OutputHandler
from src.output.mongo_output_handler import  MongoOutputHandler

from src.transformer import Transform
from src.transform.identity_transform import IdentityTransformer
from src.transform.reference_transform import ReferenceTransformer
from src.transform.dynamic_transform import DynamicTransformer

from src.misc.memory_cache import MemoryCache
from src.transform import identity_transform


class Factory(object):

    def create_input_provider(ihandler, man: dict) -> InputProvider:
        p = None
        if 'type' in man:
            type = man['type'].upper()

            if type == 'CSV':
                p = CSVInputProvider(ihandler, man)
            elif type == 'LINE':
                p = LineBasedInputProvider(ihandler, man)
            elif type == 'HTTP':
                p = HttpInputProvider(ihandler, man)
            elif type == 'MONGODB':
                p = MongoDBInputProvider(ihandler, man)
            elif type == 'MYSQL':
                p = MYSQLInputProvider(ihandler, man)
            elif type == 'POSTGRES':
                p = Psycopg2InputProvider(ihandler, man)
            elif type == 'ATHENA':
                p = AthenaInputProvider(ihandler, man)
            elif type == 'RANGE':
                p = RangeInputProvider(ihandler, man)
            elif type == 'TEMPLATE_LIST':
                p = TemplateListInputProvider(ihandler, man)
            else:
                raise ValueError (f'Unrecognized Input Provider [{type}].')
        else:
            raise ValueError ('Type is not specified in the input configuration.')

        return p

    def create_output_handler(man: dict) -> OutputHandler:
        p = None
        if 'type' in man:
            type = man['type'].upper()

            if type == 'CSV':
                p = CSVOutputHandler(man)
            elif type == 'UNIQUE_CSV':
                p = UniqueCSVOutputHandler(man)
            elif type == 'JSON':
                p = JsonOutputHandler(man)
            elif type == 'POSTGRES':
                p = Psycopg2OutputHandler(man)
            elif type == 'COMPOSITE':
                p = CompositeOutputHandler(man)
            elif type == 'MONGODB':
                p = MongoOutputHandler(man)
            else:
                raise ValueError (f'Unrecognized Input Provider [{type}].')
        else:
            raise ValueError ('Type is not specified in the input configuration.')

        return p

    def create_transformer (man: dict) -> Transform:
        t = None
        if 'type' in man:
            type = man['type'].upper()
            if type == 'REFERENCE' or type == 'DEFAULT':
                t = ReferenceTransformer(man)
            elif type == 'IDENTITY':
                t = IdentityTransformer(man)
            elif type == 'DYNAMIC':
                t = DynamicTransformer(man)
            else:
                raise ValueError(f'Unrecognized Input Provider [{type}].')
        else:
            raise ValueError('Type is not specified in the input configuration.')

        return t

    def create_mem_cache(man) -> MemoryCache:
        return MemoryCache(man)
