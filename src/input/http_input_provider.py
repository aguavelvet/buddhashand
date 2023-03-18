from flask import Flask
from flask import request

from ..input_handler import InputHandler
from ..input_provider import InputProvider

app = Flask(__name__)
s_inputProvider = None


@app.route('/')
def index():
    return 'Its alive!!!'

@app.route('/ping')
def ping():
    return 'Pong ...'


@app.route('/transform', methods=['POST'])
def transform():
    rqst = request
    return s_inputProvider.handle(rqst.json)


@app.get('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def setInputProvider(inputProvider):
    global s_inputProvider
    s_inputProvider = inputProvider


class HttpInputProvider(InputProvider):

    def __init__(self, handler: InputHandler, config: map):

        self.handler = handler
        self.config = config
        self.port = config['port'] if 'port' in config else 5000
        self.debug = config['debug'] if 'debug' in config else False

        setInputProvider(self)

    def start (self):
        '''
        start the consumption process.  This is nothing more than starting the server.
        When the server receives a command, it is forwarded to the input handler
        '''
        app.run(port=self.port,debug=self.debug)

    def handle (self,body):
        self.handler.handle(body)
        return body['OUTPUT']



    def done (self):
        '''
        stop the web server
        '''
