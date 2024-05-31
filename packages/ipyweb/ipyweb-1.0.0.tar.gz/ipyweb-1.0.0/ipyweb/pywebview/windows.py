import os
import re
import sys
from ipyweb.app import app
from ipyweb.config import config
from ipyweb.logger import logger
from ipyweb.utils import utils
from ipyweb.contracts.ipywebException import ipywebException
from ipyweb.event import event


class windows:

    def run(self, windowsParams={}, **event):
        self.windowsIpyweb = windowsIpyweb()
        return (
            self.windowsIpyweb._setParams(windowsParams)  # 设置参数
            ._setOnStarted(event.get('onStarted', None))  # 窗口打开事件
            ._setOnCreated(event.get('onCreated', None))  # 窗口创建事件
            ._setOnCreateBefore(event.get('onCreateBefore', None))  # 窗口创建之前
            ._setOnStartBefore(event.get('onStartBefore', None))  # 窗口启动之前
            ._run()
        )


class windowsIpyweb:
    _params = {
        'title': 'ipyweb',
        'url': '',
        'html': '',
        'width': 400,
        'height': 750,
        'x': None,
        'y': None,
        'resizable': False,
        'min_size': (400, 800),
        'text_select': False,
        'confirm_close': False,
        'on_top': False,
        'frameless': False,
        'easy_drag': False,
        'minimized': False,
        'shadow': False,
        'focus': False,
        'zoomable': False,
        'vibrancy': False,
        'background_color': '#FFFFFF',
        'transparent': False,
        'hidden': False,
        'fullscreen': False,
        'server': None,
        'server_args': {},

        'func': None,
        'args': None,
        'private_mode': False,
        'localization': {},
        'storage_path': '',
        'debug': False,
        'http_server': False,
        'http_port': 8080,
        'user_agent': None,
        'gui': '',
        'menu': [],
        'ssl': False
    }
    _createParams = {},
    _startParams = {}
    _supportWindowsParams = ['title', 'url', 'html', 'width', 'x', 'y', 'resizable', 'min_size', 'confirm_close',
                             'on_top',
                             'frameless',
                             'easy_drag', 'minimized', 'shadow', 'focus', 'zoomable', 'vibrancy', 'background_color',
                             'transparent', 'hidden', 'fullscreen', 'server', 'server_args', 'js_api']
    _supportStartsParams = ['func', 'args', 'private_mode', 'localization', 'storage_path', 'debug', 'http_server',
                            'http_port', 'user_agent', 'gui', 'menu', 'server', 'server_args', 'ssl']
    _tartget = {}
    _onCreateBefore = None
    _onCreated = None
    _onStartBefore = None
    _onStarted = None
    name = 'main'
    windows = None

    def _run(self):

        self._parseParams()
        _checkParams = self._checkParams()
        if _checkParams != True and type(_checkParams) == str:
            return _checkParams
        try:
            import webview
            event.emit('windows_createBefore', self, name=self.name, windows=self.windows)  # 创建之前事件
            if callable(self._onCreateBefore): self._onCreateBefore(self)  # 创建之前回调
            if self._tartget.get('enable', False):
                self._createParams = dict(self._createParams, **{
                    "html": self._tartget.get('html', ''),
                    "url": self._tartget.get('url', ''),
                })
            self.windows = webview.create_window(**self._createParams)  # 创建窗口
            event.emit('windows_created', self, name=self.name, windows=self.windows)  # 创建成功事件
            if callable(self._onCreated): self._onCreated(self)  # 创建成功回调

            self._settingsUpdate()  # 设置窗口实例及更新配置
            self._startParams = dict(self._params, **{
                'func': self._onStartedCallable,
                'args': self,
                'storage_path': os.path.normpath(f'{app.runtimePath}/{str(self._params.get("storage_path", "cache"))}'),
            })
            if callable(self._onStartBefore): self._onStartBefore(self)
            event.emit('windows_startBefore', self, name=self.name, windows=self.windows)
            self._startParams = {k: v for k, v in self._startParams.items() if k in self._supportStartsParams}
            if self._tartget.get('enable', False):
                self._startParams = dict(self._startParams, **{
                    "http_server": False,
                })
            webview.start(**self._startParams)  # 启动窗口

        except Exception as e:
            ipywebException(f'窗口[{self.name}]打开异常:{e}')
            return f'窗口[{self.name}]打开异常:{e}'

    def _onStartedCallable(self, winCls):
        event.emit('windows_started', winCls, name=self.name, windows=self.windows)
        if callable(self._onStarted): self._onStarted(winCls)

    def setStartParams(self, startParams={}):
        self._startParams = dict(self._startParams, **startParams)
        return self

    def setCreateParams(self, createParams={}):
        self._createParams = dict(self._createParams, **createParams)
        return self

    def _parseParams(self):
        if self._params.get('target', False):
            self._tartget = {
                'enable': True,
                "html": self._params.get('html', ''),
                "url": self._params.get('url', ''),
                'http_server': False
            }
        self._createParams = {k: v for k, v in self._params.items() if k in self._supportWindowsParams}

        return self

    def _setParams(self, params={}):
        self._params = config.get('windows', {})
        self._params = dict(self._params, **params)
        self.name = self._params.get('name', 'main')
        return self

    def _checkParams(self) -> bool or str:
        try:
            if self.name == '' or (self._tartget.get('enable', False) and self.name == 'main'):
                return f'窗口名称必须并保持唯一'
            self.name = re.sub(r'[^A-Za-z0-9]', '', self.name)
            if self.name == '':
                return f'窗口名称只能是大小写字母和数字'
        except Exception as e:
            return f'打开窗口参数检测异常: {e}'
        return True

    def _setOnStartBefore(self, onStartBefore=None):
        if callable(onStartBefore):
            self._onStartBefore = onStartBefore
        return self

    def _setOnCreateBefore(self, onCreateBefore=None):
        if callable(onCreateBefore):
            self._onCreateBefore = onCreateBefore
        return self

    def _setOnCreated(self, onCreated=None):
        if callable(onCreated):
            self._onCreated = onCreated
        return self

    def _setOnStarted(self, onStarted=None):
        if callable(onStarted):
            self._onStarted = onStarted
        return self

    def _settingsUpdate(self):
        import webview
        webview_settings = self._params.get('webview_settings', {})
        if webview_settings and len(webview_settings):
            for key, value in webview_settings.items():
                webview.settings[key] = value
        if utils.isWin() and utils.isModuleInstalled('cefpython3') and config.get('windows.gui', '') == 'cef':
            # To pass custom settings to CEF, import and update settings dict
            # See the complete set of options for CEF, here: https://github.com/cztomczak/cefpython/blob/master/api/ApplicationSettings.md
            try:
                from webview.platforms.cef import settings, browser_settings
                settings.update(self._params.get('cef_settings', {}).get('settings', {}))
                browser_settings.update(self._params.get('cef_settings', {}).get('browser_settings', {}))
            except Exception as e:
                pass
