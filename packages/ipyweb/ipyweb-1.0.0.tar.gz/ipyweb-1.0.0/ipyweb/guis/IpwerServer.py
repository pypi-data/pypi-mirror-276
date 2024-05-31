from ipyweb.app import app
from ipyweb.event import event
from ipyweb.logger import logger
from ipyweb.service import service


class IpywebServer:
    _config = {}
    url = ''

    def __init__(self, httpConfig={}):
        self._config = dict(self._config, **httpConfig)

    def run(self):
        event.on('windows_createBefore', self._onWindowsCreateBefore)
        event.on('windows_startBefore', self._onWindowsStartBefore)

    def _onWindowsCreateBefore(self, winCls, **kwargs):
        if kwargs.get('name', '') == 'main':
            server_args = {}
            if self._config.get('ssl', False):
                from webview import generate_ssl_cert
                keyfile, certfile = generate_ssl_cert()
                server_args['keyfile'] = keyfile
                server_args['certfile'] = certfile

            winCls.setCreateParams({
                'url': IpywebBottleServer.start(self._config),
                'http_port': self._config.get('http_port', 8090),
                'server_args': server_args
            })

    def _onWindowsStartBefore(self, winCls, **kwargs):
        pass


class IpywebBottleServer:
    def __init__(self) -> None:
        import uuid
        self.root_path = '/'
        self.running = False
        self.address = None
        self.js_callback = {}
        self.js_api_endpoint = None
        self.uid = str(uuid.uuid1())

    @classmethod
    def start(self, config={}):
        import json
        server = self()

        import bottle
        server.root_path = app.path(app.realResourcesPath)
        bottleApp = bottle.Bottle()

        @bottleApp.post(f'/js_api/{server.uid}')
        def js_api():
            bottle.response.headers['Access-Control-Allow-Origin'] = '*'
            bottle.response.headers[
                'Access-Control-Allow-Methods'
            ] = 'PUT, GET, POST, DELETE, OPTIONS'
            bottle.response.headers[
                'Access-Control-Allow-Headers'
            ] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

            body = json.loads(bottle.request.body.read().decode('utf-8'))
            if body['uid'] in server.js_callback:
                return json.dumps(server.js_callback[body['uid']](body))
            else:
                logger.console.error('JS callback function is not set for window %s' % body['uid'])

        @bottleApp.route('/')
        def index():
            import webview
            return bottle.template(
                app.path(app.realResourcesPath + '/' + config.get('index_html', 'index.html')), token=webview.token)

        @bottleApp.route('/<file:path>')
        def asset(file):
            if not server.root_path:
                return ''
            bottle.response.set_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            bottle.response.set_header('Pragma', 'no-cache')
            bottle.response.set_header('Expires', 0)
            if file.endswith('.js'):
                return bottle.static_file(file, root=server.root_path, mimetype="application/javascript")
            else:
                return bottle.static_file(file, root=server.root_path)

        httpControllers = service.module('app.httpControllers', True, True)
        for name, controller in httpControllers.items():
            # 开始注册路由
            attributes = dir(controller)
            methods = [
                attr for attr in attributes if
                callable(getattr(controller, attr)) and not attr.startswith('__') and attr not in [
                    'windows', 'registerRoute']
            ]
            for method in methods:
                if callable(getattr(controller, method)):
                    bottleApp.route(f'/{name}/{method}', ['GET', 'POST'])(getattr(controller, method))

        return bottleApp
