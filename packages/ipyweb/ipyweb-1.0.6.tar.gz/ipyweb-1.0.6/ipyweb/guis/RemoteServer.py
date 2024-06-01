from ipyweb.event import event
from ipyweb.utils import utils

class RemoteServer:
    _config = {}

    def __init__(self, httpConfig={}):
        self._config = dict(self._config, **httpConfig)

    def run(self):
        event.on('windows_createBefore', self._onWindowsCreateBefore)
        event.on('windows_startBefore', self._onWindowsStartBefore)
        event.on('windows_started', self._onWindowsStarted)

    def _onWindowsStarted(self, winCls, **kwargs):
        if self._config.get('loading', False) and kwargs.get('name', '') == 'main':
            from ipyweb.addons.loadingGui import loadingGui
            loadingGui.redirect(winCls, self._config.get('url'))

    def _onWindowsCreateBefore(self, winCls, **kwargs):
        if kwargs.get('name', '') == 'main':
            if self._config.get('loading', False):
                from ipyweb.addons.loadingGui import loadingGui
                loadingGui.load(winCls)
            else:
                winCls.setCreateParams({
                    'url': self._config.get('url', ''),
                })

    def _onWindowsStartBefore(self, winCls, **kwargs):
        if kwargs.get('name', '') == 'main':
            winCls.setStartParams({
                'http_server': self._config.get('http_server', False),
                'http_port': self._config.get('http_port', 8090),
                'ssl': self._config.get('ssl', False),
            })
