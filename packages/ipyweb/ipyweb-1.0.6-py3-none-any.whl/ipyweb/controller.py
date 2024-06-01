import re
import importlib
from ipyweb.app import app
from ipyweb.utils import utils
from ipyweb.config import config
from ipyweb.singleton import singleton
from ipyweb.event import event


class controller(metaclass=singleton):
    _controllers = {}  # 所有控制器
    _windows = {}  # 打开的所有窗口对象
    _windowExists = {}  # 存在的老窗口

    @classmethod  # 由controllerPreload预载入模块负责载入所有控制器类
    def _load(self, controllers={}):
        self._controllers = controllers
        event.on('windows_createBefore', self._onWindowsCreateBefore)
        event.on('windows_created', self._onWindowsCreated)
        return self

    @classmethod
    def _getWindows(self, name=''):
        return self._windows[name] if name in self._windows else self._windows

    @classmethod  # windows窗口已创建
    def _onWindowsCreateBefore(self, winCls, **kwargs):
        winCls.setCreateParams({
            'js_api': self()
        })

        return self

    @classmethod  # windows窗口已创建
    def _onWindowsCreated(self, winCls, **kwargs):
        if winCls.name and winCls.windows:
            name = winCls.name
            windows = winCls.windows
            self._windows[name] = windows
            if hasattr(controllerEventer, 'run'):
                controllerEventer.run(name, windows)

        return self

    def invoke(self, spacename='', *args):
        import webview
        windowName = ''
        controllerName = ''
        try:
            windowName, controllerName, actionName = controllerParser.parseSpaceName(spacename)
            isTarget, targetName = controllerParser.isTargetWindow(args)
            handleWindow = self._windows.get(windowName, None)  # 操作窗口
            targetWindow = self._windows.get(targetName, None)  # 打开的新窗口
            handleWindowExist = isinstance(handleWindow, webview.window.Window)
            targetWindowExist = isinstance(targetWindow, webview.window.Window)

            if handleWindowExist != True and isTarget == False:
                return controllerEventer._error(f'window[{windowName}] does not exist')

            # 同名窗口已存在则销毁 如需不销毁请自行维护窗口不同名称
            if isTarget and targetWindowExist and hasattr(targetWindow, 'destroy'): targetWindow.destroy()
            if self._controllers.get(controllerName, ''):
                controllerInvoke = self._controllers[controllerName]
                if callable(getattr(controllerInvoke, actionName, None)):
                    methodInvoke = getattr(controllerInvoke, actionName)
                    return methodInvoke(handleWindow, *args)
                else:
                    return controllerEventer._error(
                        f'window[{windowName}]controller[{controllerName}]method[{actionName}] does not exist')
            else:
                return controllerEventer._error(f'window[{windowName}]controller[{controllerName}]does not exist')
        except Exception as e:
            return controllerEventer._error(
                f'An exception occurred while executing window[{windowName}]controller[{controllerName}]:{e}')


class controllerEventer(metaclass=singleton):
    @classmethod
    def run(self, name='', window=None):
        self._loadWindowEvents(name, f'ipyweb.{app.windowEventsName}.{name}', window)
        if config.get('app.autoLoad.loadWindowEventsEnable', True):
            self._loadWindowEvents(name, f'app.{app.getName()}.{app.backendName}.{app.windowEventsName}.{name}', window)
        return self

    @classmethod
    def _loadWindowEvents(self, name='', moduleName='', window=None):
        try:
            envents = ['closed', 'closing', 'shown', 'loaded', 'minimized', 'maximized', 'restored', 'resized', 'moved']

            className = moduleName.split('.')[-1]
            rootPrefix = app.ipywebRootPath if moduleName.startswith(app.ipywebPath) else app.rootPath
            module = utils.smartImportModule(className, moduleName, rootPrefix)
            if module and hasattr(module, name):
                moduleAttr = getattr(module, name)
                moduleInstance = moduleAttr()
                for envent in envents:
                    self._addOnEvent(moduleInstance, window, envent)
        except Exception as e:
            pass
        return self

    @classmethod
    def _addOnEvent(self, moduleInstance=None, window=None, fn=''):

        if hasattr(moduleInstance, fn) and callable(getattr(moduleInstance, fn)):
            fnInstance = getattr(moduleInstance, fn)
            if fn == 'closed': window.events.closed += fnInstance
            if fn == 'closing': window.events.closing += fnInstance
            if fn == 'shown': window.events.shown += fnInstance
            if fn == 'loaded':  window.events.loaded += fnInstance
            if fn == 'minimized': window.events.minimized += fnInstance
            if fn == 'maximized': window.events.maximized += fnInstance
            if fn == 'restored': window.events.restored += fnInstance
            if fn == 'resized': window.events.resized += fnInstance
            if fn == 'moved': window.events.moved += fnInstance
        return self

    @classmethod
    def _error(self, msg='error', data={}, code=1):
        return self._json(code, msg, data)

    @classmethod
    def _success(self, msg='success', data={}):
        return self._json(0, msg, data)

    @classmethod
    def _json(self, code=0, msg='success', data={}):
        return {
            'code': code,
            'message': msg,
            'data': data
        }


class controllerParser():
    @classmethod
    def parseSpaceName(self, spacename=''):
        windowName = 'main'
        controllerName = 'app'
        actionName = 'index'
        try:
            spacename = re.sub(r'[^A-Za-z0-9/@_]', '', spacename)
            _spacenames = spacename.split('/')
            if len(_spacenames) >= 1: controllerName = _spacenames[0]
            if len(_spacenames) >= 2: actionName = _spacenames[1]
            _actions = actionName.split('@')
            if len(_actions) >= 1: actionName = _actions[0]
            if len(_actions) >= 2 and _actions[1] != '': windowName = _actions[1]
        except Exception as e:
            pass

        return windowName, controllerName, actionName

    @classmethod  # 是否新窗口打开
    def isTargetWindow(self, args):
        isTarget = False  # 是否新窗口打开
        targetName = ''  # 新窗口名称
        try:
            if len(args) > 0 and type(args[0]) == dict:
                if args[0].get('target', False) == True: isTarget = True
                targetName = args[0].get('name', '')
        except Exception as e:
            pass
        return isTarget, targetName
