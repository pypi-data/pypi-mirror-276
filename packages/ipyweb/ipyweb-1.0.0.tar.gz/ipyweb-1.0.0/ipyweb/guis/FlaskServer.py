
from ipyweb.app import app
from ipyweb.event import event
from ipyweb.service import service
from ipyweb.singleton import singleton
from flask import Flask, render_template, Blueprint
from webview import generate_ssl_cert

class FlaskServer(metaclass=singleton):
    _config = {}
    flask = None
    _supportParams = ['import_name', 'root_path', 'instance_relative_config', 'instance_path',
                      'subdomain_matching', 'host_matching', 'static_host',
                      'static_folder', 'static_url_path', 'static_folder', 'template_folder']

    def __init__(self, httpConfig={}):
        self._config = dict(self._config, **httpConfig)

    def run(self):
        event.on('windows_createBefore', self._onWindowsCreateBefore)
        event.on('windows_startBefore', self._onWindowsStartBefore)

    def _onWindowsCreateBefore(self, winCls, **kwargs):

        if kwargs.get('name', '') == 'main':
            server_args = {}
            if self._config.get('ssl', False):
                keyfile, certfile = generate_ssl_cert()
                server_args['keyfile'] = keyfile
                server_args['certfile'] = certfile
            winCls.setCreateParams({
                'url': self.loadFlask(),
                'http_port': self._config.get('http_port', 8090),
                'server_args': server_args
            })

    def _onWindowsStartBefore(self, winCls, **kwargs):
        if kwargs.get('name', '') == 'main':
            winCls.setStartParams({
                'http_server': False,  # 是否开启http服务器
            })

    def loadFlask(self):
        flaskConfig = dict(self._config, **{
            'import_name': __name__,
            'static_folder': app.path(app.realResourcesPath + '/' + self._config.get('static_folder', 'assets')),
            'template_folder': app.realResourcesPath,
        })
        flaskConfig = {k: v for k, v in flaskConfig.items() if k in self._supportParams}
        self.flask = Flask(**flaskConfig)
        self._registerRoute()
        return self.flask

    def _registerRoute(self):

        @self.flask.route('/')
        def index():
            import webview
            return render_template(self._config.get('index_html', 'index.html'), token=webview.token)

        # 更改js文件的返回头
        @self.flask.after_request
        def changeHeader(response):
            disposition = response.get_wsgi_headers('environ').get('Content-Disposition') or ''
            if disposition.endswith('.js'):
                response.mimetype = 'application/javascript'
            return response

        httpControllers = service.module('app.httpControllers', True, True)
        for name, controller in httpControllers.items():
            # 注册蓝图
            if controller.blueprint and isinstance(controller.blueprint, Blueprint) and self._config.get(
                    'controllerBlueprint', False) == True:
                controller.blueprint.name = name
                self.flask.register_blueprint(controller.blueprint, url_prefix='/' + controller.blueprint.name)
            # 开始注册路由
            attributes = dir(controller)
            methods = [
                attr for attr in attributes if
                callable(getattr(controller, attr)) and not attr.startswith('__') and attr not in [
                    'windows', 'registerRoute']
            ]
            for method in methods:
                if callable(getattr(controller, method)):
                    self.flask.add_url_rule(
                        rule=f'/{name}/{method}',
                        methods=['POST', 'GET'],
                        view_func=getattr(controller, method)
                    )
        return self
