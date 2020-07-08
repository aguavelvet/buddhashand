import os
from src.transformer import Transform
from src.transform.functors import get_fn_registry


from simpleeval import simple_eval
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

    def transform (self, rec:dict) -> dict:

        self._update_namespace(rec)

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
                out[t[0]] = self.simple_eval.eval(t[1])

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


