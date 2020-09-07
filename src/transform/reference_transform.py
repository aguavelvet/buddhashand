import os
from src.transformer import Transform
from src.transform.functors import get_fn_registry
from simpleeval import SimpleEval


class ReferenceTransformer(Transform):

    def __init__(self, cfg:map):

        self.template = cfg['transform']
        self.prefilter = cfg['prefilter'] if 'prefilter' in cfg else None
        # instantiate the simple evaluator.  Add our own registry as well.
        self.simple_eval = SimpleEval()
        self.simple_eval.functions.update(get_fn_registry())

        # update the name space with runtime configuration variables as well. say -DDEBUG=verbose or something like it.
        self._update_namespace(os.environ)


    def get_namespace_rec (self, tmap, irec):
        orec = {}
        for k,t in tmap.items():
            # print (f' out field name = {k} in field name = {t} and value = {irec[t]}')
            # print(irec)
            # if k == 'operation_name':
            #    print (f'Oh oh...... [{irec[t]}]')

            # condition the output field value.  simple parser does not like ''
            v = irec[t]
            v = '' if v is None else str(v).strip()
            orec[k] = '' if v == '' else self.simple_eval.eval(v)

        print (orec)
        return orec


    def transform (self, irec:dict) -> dict:

        self._update_namespace(irec)

        # if prefilter is defined, pre-filter the record first.
        # run the evaluation.  We are creating an output record  using the template known_directives and the
        # input values found in the in put record.  each field in the input record is updated in name space.
        filtered_in = True
        if self.prefilter is not None and self.prefilter != '':
            filtered_in = self.simple_eval.eval(self.prefilter)

        out = None
        if filtered_in:
            out = {}
            for t in self.template.items():
                if len(t) != 2:
                    raise ValueError (f'Could not retrieve key/value pair in transform template [{t}]. ')

                if type(t[1]) is str:
                    out[t[0]] = self.simple_eval.eval(t[1])
                elif type(t[1]) is dict:
                    out[t[0]] = self.get_namespace_rec (t[1], irec)
                else:
                    # TODO  Should make sure that the template is either namespace based or not. Cant mix.
                    raise ValueError (f'Unhandled template type {type(t[1])}')


        return out


    def _update_namespace (self, rec):
        '''
        update the evaluator name space with all the fields.  These values are then available to the expression parser
        as REC.FieldName
        :param rec: input record
        :return:
        '''

        for field in rec.items():

            if type(field[1]) is str:
                self.simple_eval.names[field[0].strip()] = field[1].strip()
            else:
                self.simple_eval.names[field[0].strip()] = field[1]


if __name__ == "__main__":

    r = get_fn_registry()
    e = SimpleEval()
    e.functions.update(r)

    e.names['a'] = 3
    e.names['b'] = 4



    print(e.eval('1 + 3'))
    print (e.eval("'A' if a > b else 'B'"))
    print (e.eval("'A' if a < b else 'B'"))
    print (e.eval('unity(1 + 3)'))
    print (e.eval('inverse (1 + 3)'))
    print (e.eval('a'))
    print (e.eval('b'))


