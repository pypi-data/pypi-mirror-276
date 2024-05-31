import os.path
from ipyweb.app import app
from ipyweb.event import event
from ipyweb.logger import logger


class LocalServer:
    _config = {}

    def __init__(self, httpConfig={}):
        self._config = dict(self._config, **httpConfig)

    def run(self):
        event.on('windows_createBefore', self._onWindowsCreateBefore)
        event.on('windows_startBefore', self._onWindowsStartBefore)

    def _onWindowsCreateBefore(self, winCls, **kwargs):
        if kwargs.get('name', '') == 'main':
            try:
                html = app.path(app.realResourcesPath + '/' + self._config.get('html', ''))
                if os.path.exists(html):
                    with open(html, 'r', encoding='utf-8') as file:
                        html = file.read()
                else:
                    html = 'The local HTML file does not exist.'
                winCls.setCreateParams({
                    'url': '',
                    'html': html
                })
            except Exception as e:
                logger.console.error(f'An exception occurred while reading the local HTML file:{e}')

    def _onWindowsStartBefore(self, winCls, **kwargs):
        if kwargs.get('name', '') == 'main':
            winCls.setStartParams({
                'http_server': self._config.get('http_server', False),
                'http_port': self._config.get('http_port', 8090),
                'ssl': self._config.get('ssl', False),
            })
