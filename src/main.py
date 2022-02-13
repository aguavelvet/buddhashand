'''
Copyright 2020 Kirby Kim

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public 
License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any 
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied 
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, 
see <http://www.gnu.org/licenses/>.
'''

import getopt, sys
import json
from src.buddhashand import Buddhashand




def usage (msg = None, ec = None):
    print('Buddhashand --manifest(-m) manifest.json [--help(-h) --verbose(-v)]')
    print('  Synopsis:')
    print('    Perform the sed like extraction or transformation specified by the manifest file. ')
    print('    Buddhas hand could be thought of as a record based highly flexible extraction/transformation tool.')
    print('    The flexibility comes from decoupling the input and output handlers and with the support of simple ')
    print('    expression parsing.  ')
    print('    Secondly, the tool is highly extensible.  The tool users can add in custom functions to drive ')
    print('    additional functionality. ')
    print('    The readers is referred to https://github.com/aguavelvet/buddhashand for additional information.')
    print('  Synopsis:')
    print('    --manifest (-m)  Manifest file that provides the necessary information for the run. The buddhashand')
    print('        *  input provider.  Input provider defines the input object that knows how to read in the input')
    print('           There are three reference implementations of input providers.  (CSV, SQL, NoSQL, HTTP)')
    print('        *  transform. Transform object provides the transformation steps as specified in the manifest.')
    print('        *  output. Output provider "Persists" the given transformed record to the persistence layer. ')
    print('        *  Reference implementations include, CSV, JSON ')
    print('    By mixing the input and output providers, we get a very rich set of functionality.  Moreover, with')
    print('    expression evaluator support, it is possible to perform some intresting transformations.  ')
    print('  Examples:  ')
    print('    1)  Read from a relational database and save as a CSV.')
    print('    2)  Read from a NoSQL database and save to a JSON file.')
    print('    2)  Perform either of 1 or 2, and add a calculated new field. ')

    sys.exit(ec)


# ----------------------------------------------------------------------------------------------------------------------
if "__main__" == __name__:
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm:v", ["help", "manifest=", "verbose"])

        manifest = None
        verbose = False
        for o, a in opts:
            if o == "-v":
                verbose = True
            elif o in ("-h", "--help"):
                usage()
                sys.exit()
            elif o in ("-m", "--manifest"):
                manifest = a
            else:
                usage (f'unhandled option {o}', 2)

        if manifest is None:
            usage ('Required parameter (manifest) was not specified.', 2)

        man = json.load(open(manifest, 'r'))

        hand = Buddhashand(man)
        hand.process()

    except getopt.GetoptError as err:
        print (str(err))  # will print something like "option -a not recognized"
        usage(2)


