import os
import sys
from pathlib import Path
from ipyweb.singleton import singleton
from ipyweb.utils import utils


class app(metaclass=singleton):
    ver = '1.0.3'
    ipywebPath = 'ipyweb'
    appPath = 'app'
    rootPath = ''
    workRootPath = ''
    ipywebRootPath = ''
    appResourcesPath = ''
    exeResourcesPath = ''
    realResourcesPath = ''
    isExe = False
    runtimePath = ''
    backendName = 'backend'
    frontendName = 'frontend'
    addonsName = 'addons'
    configsName = 'configs'
    controllersName = 'controllers'
    httpControllersName = 'httpControllers'
    eventsName = 'events'
    servicesName = 'services'
    preloadsName = 'preloads'
    commandsName = 'commands'
    socketsName = 'sockets'
    queuesName = 'queues'
    databasesName = 'databases'
    resourcesName = 'resources'
    ipywebAutoConfigName = 'ipywebAutoConfig'
    timersName = 'timers'
    windowEventsName = 'windowEvents'
    moduleJsonFileName = 'modules'
    bulidPathName = 'build'
    lifecycleDebug = False

    name = os.environ.get('appName', '')
    version = int(ver.replace('.', ''))

    def __init__(self):
        if appIpyweb._loaded == False: appIpyweb.load()

    @classmethod
    def getName(self):
        return self.name

    @classmethod
    def setName(self, name=''):
        try:
            self.name = name if name else self.name
            if self.name == '' and len(sys.argv) >= 2:
                self.name = sys.argv[1]
            appIpyweb._setSourcePath()  # 重置资源文件路径
        except Exception as e:
            pass
        return self

    @classmethod
    def path(self, path='', root=False):
        return os.path.normpath(f'{self.rootPath}/{path}') if root else os.path.normpath(f'{path}')


class appIpyweb(metaclass=singleton):
    _loaded = False
    _resourcesName = ''

    @classmethod
    def load(self, reload=False):
        if self._loaded == False or reload == True:
            self._setBasePath()._setSourcePath()
            if app.lifecycleDebug:
                print('::::::::::::::::::::::::::app loaded::::::::::::::::::::::::::')
            self._loaded = True
        return self

    @classmethod
    def reload(self):
        self.load(True)
        return self

    @classmethod
    def _setSourcePath(self):
        try:
            # 资源目录
            app.exeResourcesPath = os.path.normpath(f'{app.workRootPath}/{app.resourcesName}')
            app.appResourcesPath = os.path.normpath(
                f'{app.rootPath}/{app.appPath}/{app.getName()}/{app.resourcesName}'
            )
            if utils.pathExists(os.path.normpath(app.exeResourcesPath)):
                app.realResourcesPath = app.exeResourcesPath
                app.isExe = True
            else:
                app.realResourcesPath = app.appResourcesPath
        except Exception as e:
            self.loaded = False
        return self

    @classmethod
    def _setBasePath(self):
        try:

            app.rootPath = str(os.getcwd())  # 根目录
            app.workRootPath = str(Path(__file__).resolve().parent.parent)  # 工作目录
            app.ipywebRootPath = app.workRootPath
            # 临时目录
            app.runtimePath = os.path.normpath(f'{app.rootPath}/runtime')
            self._createDir(app.runtimePath)
        except Exception as e:
            self.loaded = False
        return self

    @classmethod
    def _createDir(self, path='', exist_ok=True):
        try:
            os.makedirs(path, exist_ok=exist_ok)
        except OSError as e:
            self.loaded = False
