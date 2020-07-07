
from ..input_provider import InputProvider
from ..output_handler import OutputHandler

from src.input.csv_input_provider import CSVInputProvider
from src.input.http_input_provider import HttpInputProvider
from src.input.nosql_input_provider import NOSQLInputProvider
from src.input.sql_input_provider import SQLInputProvider

from src.output.csv_output_handler import CSVOutputHandler
from src.output.json_output_handler import JsonOutputHandler

from src.transformer import Transform
from src.transform.identity_transform import IdentityTransformer
from src.transform.reference_transform import ReferenceTransformer


from src.transform import identity_transform

class Factory(object):


    def create_input_provider (ihandler, man:dict) -> InputProvider:
        p = None
        if 'type' in man:
            type = man['type'].upper()

            if type == 'CSV':
                p = CSVInputProvider(ihandler, man)
            elif type == 'HTTP':
                p = HttpInputProvider(ihandler, man)
            elif type == 'NOSQL':
                p = NOSQLInputProvider(ihandler, man)
            elif type == 'SQL':
                p = SQLInputProvider(ihandler, man)
            else:
                raise ValueError (f'Unrecognized Input Provider [{type}].')
        else:
            raise ValueError ('Type is not specified in the input configuration.')

        return p


    def create_output_handler (man: dict) -> OutputHandler:
        p = None
        if 'type' in man:
            type = man['type'].upper()

            if type == 'CSV':
                p = CSVOutputHandler(man)
            elif type == 'JSON':
                p = JsonOutputHandler(man)
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
            else:
                raise ValueError(f'Unrecognized Input Provider [{type}].')
        else:
            raise ValueError('Type is not specified in the input configuration.')

        return t
