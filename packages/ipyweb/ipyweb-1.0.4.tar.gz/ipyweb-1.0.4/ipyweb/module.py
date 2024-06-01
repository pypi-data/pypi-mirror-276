import os
from functools import lru_cache
from ipyweb.app import app, appIpyweb
from ipyweb.logger import logger, loggerIpyweb
from ipyweb.utils import utils
from ipyweb.singleton import singleton
from ipyweb.config import config, configIpyweb
from ipyweb.jsonFile import jsonFile


class module(metaclass=singleton):
    cfgKey = app.moduleJsonFileName

    def __init__(self):
        if appIpyweb._loaded == False: appIpyweb.load()
        if loggerIpyweb._loaded == False: loggerIpyweb.load()
        if configIpyweb._loaded == False: configIpyweb.load()
        if moduleIpyweb._loaded == False: moduleIpyweb.load()

    @classmethod
    def maps(self, name='ipyweb', default=None, reload=False):
        try:
            if reload: moduleIpyweb.reload()
            return config.get(f'{self.cfgKey}.maps.{name}', default)
        except Exception as e:
            logger.console.error(f'An exception occurred while retrieving dynamic module maps：{e}')
        return {}

    @classmethod
    def modules(self, reload=False):
        try:
            if reload: moduleIpyweb.reload()
            modules = config.get(f'{self.cfgKey}.modules', [])
            return modules
        except Exception as e:
            logger.console.error(f'An exception occurred while retrieving the dynamic module：{e}')
        return []

    @classmethod
    def jsonFileMaps(self, name='', default=None):
        try:
            moduleIpyweb._getJsonFileModules()
            return config.get(f'{self.cfgKey}.maps.{name}', default)
        except Exception as e:
            logger.console.error(f'An exception occurred while retrieving dynamic module maps：{e}')
        return {}


class moduleIpyweb(metaclass=singleton):
    # 自动载入目录
    _dirs = [
        f'{app.addonsName}',
        f'{app.commandsName}',
        f'{app.configsName}',
        f'{app.controllersName}',
        f'{app.httpControllersName}',
        f'{app.eventsName}/register',
        f'{app.eventsName}/listener',
        f'{app.preloadsName}/block',
        f'{app.preloadsName}/process',
        f'{app.preloadsName}/thread',
        f'{app.servicesName}',
        f'{app.socketsName}',
        f'{app.queuesName}',
        f'{app.timersName}',
        f'{app.windowEventsName}',
    ]
    _maps = {
        'name': app.getName(),
        'app': {},
        'ipyweb': {},
    }

    _appModuleFile = ''
    _exeModuleFile = ''
    _modules = []
    _loaded = False

    def __init__(self):
        if appIpyweb._loaded == False: appIpyweb.load()
        if loggerIpyweb._loaded == False: loggerIpyweb.load()
        if configIpyweb._loaded == False: configIpyweb.load()

    @classmethod
    def load(self, relaod=False):
        if self._loaded == False or relaod == True:
            if app.isExe:
                self._getJsonFileModules()
            else:
                self._getDirFileModules()
            if app.lifecycleDebug:
                print('::::::::::::::::::::::::::module loaded::::::::::::::::::::::::::')
            self._loaded = True
        return self

    @classmethod
    def reload(self):
        self.load(True)
        return self

    @classmethod
    @lru_cache(128)
    def _getJsonFileModules(self):
        modules = {}
        try:
            # 不同来源获取的模块资源文件地址不同
            self._getModuleFilePath()
            file = self._exeModuleFile if app.isExe else self._appModuleFile
            modules = jsonFile().get(file)
            self._setConfigModules(modules)
        except Exception as e:
            logger.console.error(f'An exception occurred while saving the dynamic module:{e}')

        return modules

    @classmethod
    def _getDirFileModules(self):
        self._getModuleFilePath()._loadModulesFromDir()._createModulesFile()._setConfigModules()
        return self

    @classmethod
    def _getModuleFilePath(self):
        self._appModuleFile = app.path(f'{app.appResourcesPath}/data/{app.moduleJsonFileName}.json', False)
        self._exeModuleFile = app.path(f'{app.exeResourcesPath}/data/{app.moduleJsonFileName}.json', False)
        return self

    @classmethod
    def _setConfigModules(self, modules={}):
        if len(modules) <= 0:
            modules = {
                'maps': self._maps,
                'modules': self._modules,
            }
        config.set(app.moduleJsonFileName, modules)
        return self

    @classmethod
    def _createModulesFile(self):
        try:
            # 仅更新应用模块资源就可以了
            if app.isExe == False:
                jsonFile().set({
                    'maps': self._maps,
                    'modules': self._modules,
                }, self._appModuleFile)
        except Exception as e:
            logger.console.error(f'An exception occurred while saving the dynamic module:{e}')
        return self

    @classmethod
    @lru_cache(maxsize=128)
    def _loadModulesFromDir(self):
        if self._loaded == True:
            return self
        # 不同来源获取的模块资源文件名称不同
        appName = config.moduleMaps('name', app.getName()) if app.isExe else app.getName()

        try:
            self._modules = []
            self._modules.append(f'app.{appName}.runner')
            self._maps['name'] = appName
            for dir in self._dirs:
                ipywebFiles = self.getFiles(path=f'{app.ipywebPath}/{dir}')
                appFiles = self.getFiles(path=f'{app.appPath}/{appName}/{app.backendName}/{dir}')
                self._maps['ipyweb'][dir] = ipywebFiles
                self._maps['app'][dir] = appFiles
                if len(appFiles) > 0 and type(appFiles) == dict:
                    for name, module in appFiles.items():
                        self._modules.append(module)
                if len(ipywebFiles) > 0 and type(ipywebFiles) == dict:
                    for name, module in ipywebFiles.items():
                        self._modules.append(module)
        except Exception as e:
            logger.console.error(f'An exception occurred while reading the dynamic module directory:{e}')
            self._loaded = False
        return self

    @classmethod
    def getFiles(self, **params) -> dict:
        path = params.get('path', '')
        ext = params.get('ext', '.py')
        replaceExt = params.get('replaceExt', True)
        appendFileName = params.get('appendFileName', False)
        format = params.get('format', True)
        formatSep = params.get('formatSep', '.')
        result = {}

        if path.startswith(app.ipywebPath):
            rootPrefix = app.ipywebRootPath
        else:
            rootPrefix = app.rootPath
        absmpath = app.path(f'{rootPrefix}/{path}')

        try:
            for root, dirs, files in os.walk(absmpath):
                if '__pycache__' in dirs: dirs.remove('__pycache__')
                for file in files:

                    if file.endswith(ext):
                        file_path = os.path.join(root.replace(rootPrefix + os.sep, ''), file)
                        if format:
                            file_path = file_path.replace(os.sep, formatSep)
                        if replaceExt:
                            file_path = file_path.replace(ext, '')
                            file_name = file_path.split('.')[-1]
                        else:
                            file_name = file_path.split('.')[-2]
                        if appendFileName:
                            file_path += formatSep + file_name
                        result[file_name] = file_path
        except Exception as e:
            click.echo(f'An exception occurred while reading the module dirs:{e}')

        return result
