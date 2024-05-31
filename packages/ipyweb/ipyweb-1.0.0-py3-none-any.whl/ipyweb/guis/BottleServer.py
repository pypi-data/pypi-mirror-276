from ipyweb.app import app
from ipyweb.event import event


class BottleServer:
    _config = {}

    def __init__(self, httpConfig={}):
        self._config = dict(self._config, **httpConfig)

    def run(self):

        event.on('windows_createBefore', self._onWindowsCreateBefore)
        event.on('windows_startBefore', self._onWindowsStartBefore)

    def _onWindowsCreateBefore(self, winCls, **kwargs):
        if kwargs.get('name', '') == 'main':
            winCls.setCreateParams({
                'url': str(app.path(app.realResourcesPath + '/' + self._config.get('index_html', 'index.html'))),
            })

    def _onWindowsStartBefore(self, winCls, **kwargs):
        if kwargs.get('name', '') == 'main':
            winCls.setStartParams({
                'http_server': True,  # 是否开启http服务器
                'http_port': self._config.get('http_port', 8090),
                'ssl': self._config.get('ssl', False),
            })
