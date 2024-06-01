import glob
import importlib
import json
import os
from json import JSONDecodeError
from ipyweb.app import app, appIpyweb
from ipyweb.utils import utils
from ipyweb.singleton import singleton
from ipyweb.logger import logger, loggerIpyweb
import ipyweb.configs.app as appCfg
import ipyweb.configs.database as databaseCfg
import ipyweb.configs.logger as loggerCfg
import ipyweb.configs.windows as windowsCfg
import ipyweb.configs.jsonFile as jsonFileCfg
import ipyweb.configs.build as buildCfg


class config(metaclass=singleton):
    def __init__(self):
        if appIpyweb._loaded == False: appIpyweb.load()
        if loggerIpyweb._loaded == False: loggerIpyweb.load()
        if configIpyweb._loaded == False: configIpyweb.load()

    @classmethod
    # 获取配置
    def get(self, key='', default=None):
        configData = configIpyweb._data
        try:
            if key == '':
                return configData;
            if '.' in key:
                keys = key.split('.')
                dict = configData
                for k in keys:
                    if k in dict:
                        dict = dict.get(k, default)
                    else:
                        return default  # 如果某个键不存在，返回None
                return dict
            else:
                return configData.get(key, default)
        except Exception as e:
            return configData

    @classmethod
    def set(self, key, value):
        configIpyweb._data[key] = value
        return True

    @classmethod
    def has(self, key):
        if key in configIpyweb._data:
            return True
        else:
            return False

    @classmethod
    def delete(self, key):
        if self.has(key):
            configIpyweb._data.pop(key)
            return True
        else:
            return False

    @classmethod
    def loadYaml(self, file=''):
        return configIpyweb._loadYaml(file)

    @classmethod
    def loadModule(self, name='', modulePath=''):
        return configIpyweb._loadFromModule(name, modulePath)

    @classmethod
    def loadodules(self, modulePaths={}):
        return configIpyweb._loadFromModules(modulePaths)

    @classmethod
    def moduleMaps(self, key='', default=None):
        return self.get(f'{app.moduleJsonFileName}.maps.{key}', default)


class configIpyweb(metaclass=singleton):
    _data = {
        'app': {},
        'logger': {},
        'windows': {},
        'database': {},
        app.moduleJsonFileName: {},
    }
    _loaded = False

    @classmethod
    def load(self, reload=False):

        if self._loaded == True and reload == False:
            return self._data

        try:

            self._loadBaseConfig()
            self._loadMoudlesConfig()

            ipywebConfig = self._data[app.moduleJsonFileName].get('maps', {}).get('ipyweb', {})
            appConfig = self._data[app.moduleJsonFileName].get('maps', {}).get('app', {})
            if 'configs' in ipywebConfig:
                self._loadFromModules(ipywebConfig.get('configs', {}))
            if config.get('app.autoLoad.loadConfigsEnable', True) and 'configs' in appConfig:
                self._loadFromModules(appConfig.get('configs', {}))
            if app.lifecycleDebug:
                print('::::::::::::::::::::::::::config loaded::::::::::::::::::::::::::')
            self._loaded = True
            return self._data
        except Exception as e:
            logger.console.error(f"An exception occurred while parsing the configuration file : {e}")
            self._loaded = False

    @classmethod
    def reload(self):
        self._loaded = False
        self.load()
        return self

    @classmethod
    def _loadBaseConfig(self):
        try:
            self._data['app'] = self._pyDict(appCfg)
            self._data['jsonFile'] = self._pyDict(jsonFileCfg)
            self._data['windows'] = self._pyDict(windowsCfg)
            self._data['logger'] = self._pyDict(loggerCfg)
            self._data['database'] = self._pyDict(databaseCfg)
            self._data['build'] = self._pyDict(buildCfg)
        except Exception as e:
            logger.console.error(f"An exception occurred while obtaining basic configuration information: {e}")
            self._loaded = False

        return self

    @classmethod
    def _loadMoudlesConfig(self):
        try:
            moduleJsonFileName = app.moduleJsonFileName
            appModuleFile = app.path(f'{app.appResourcesPath}/data/{moduleJsonFileName}.json', False)
            exeModuleFile = app.path(f'{app.exeResourcesPath}/data/{moduleJsonFileName}.json', False)

            file = exeModuleFile if app.isExe else appModuleFile
            modules = self._loadModuleJson(file)
            self._data[moduleJsonFileName] = modules
        except Exception as e:
            logger.console.error(f"An exception occurred while reading module information : {e}")
            self._loaded = False

        return self

    @classmethod
    def _loadModuleJson(self, file=''):
        try:
            jsonConfig = self._data.get('jsonFile', {}).get('config', {})
            if os.path.exists(file) != True: return {}
            with open(file, 'r', encoding=jsonConfig.get('encoding', 'utf-8')) as f:
                return json.load(f)
        except Exception as e:
            logger.console.error(f"An exception occurred while reading the module file: {e}")
        except JSONDecodeError as e:
            logger.console.error(f"The data format of the module file is incorrect: {e}")
        except FileNotFoundError:
            logger.console.error("The module file does not exist")
        except PermissionError:
            logger.console.error("No permission to read the module file")
        return {}

    @classmethod
    def _pyDict(cls, module=None, default={}):
        if module is not None:
            return {name: value for name, value in module.__dict__.items() if not name.startswith("_")}
        else:
            return default

    @classmethod
    def _loadFromModule(self, name='', modulePath=''):
        try:
            rootPrefix = app.ipywebRootPath if modulePath.startswith(app.ipywebPath) else app.rootPath
            module = utils.smartImportModule(name, modulePath, rootPrefix)
            configData = self._pyDict(module)
            if configData and type(configData) == dict and len(configData) > 0:
                if self._data.get(name) is not None:
                    self._data[name] = dict(self._data[name], **configData)
                else:
                    self._data.update({name: configData})
                return True

        except ImportError as e:
            logger.console.error(f'Module [{str(modulePath)}] does not exist')
        except Exception as e:
            logger.console.error(f'An exception occurred while reading the configuration file [{str(modulePath)}]: {e}')
            self._loaded = False
        return False

    @classmethod
    def _loadFromModules(self, modulePaths={}):

        try:
            if modulePaths and type(modulePaths) == dict and len(modulePaths) > 0:
                for name, modulePath in modulePaths.items():
                    self._loadFromModule(name, modulePath)
                return True
            return False
        except Exception as e:
            logger.console.error(f'An exception occurred while reading the configuration files: {e}')
        return False

    @classmethod
    def _loadYaml(self, configFile=''):
        configData = {}
        try:
            import yaml
        except ImportError:
            logger.console.error(f'Please installer module :yaml (pip install yaml)')
            return False
        try:
            with open(configFile, 'r', encoding='utf-8') as stream:
                try:
                    configData = yaml.safe_load(stream)
                except yaml.YAMLError as e:
                    logger.console.error(f'An exception occurred while reading the yaml file: {e}')
        except Exception as e:
            logger.console.error(f'An exception occurred while opening the  yaml file: {e}')
        return configData

    @classmethod
    def _loadFromYamlDir(self, folder='', extension='*.yaml'):
        folder = os.path.normpath(folder)

        if not folder or not extension:
            return False
        try:
            import yaml
        except ImportError:
            logger.console.error(f'Please installer module :yaml (pip install yaml)')
            return False

        for configFile in glob.glob(os.path.join(folder, extension)):
            name, ext = os.path.splitext(os.path.basename(configFile))
            try:
                with open(configFile, 'r', encoding='utf-8') as stream:
                    try:
                        configData = yaml.safe_load(stream)
                        if configData and type(configData) == dict and len(configData) > 0:
                            if self._data.get(name) is not None:
                                self._data[name] = dict(self._data[name], **configData)
                            else:
                                self._data.update({name: configData})
                    except yaml.YAMLError as e:
                        logger.console.error(f'An exception occurred while reading the yaml dir: {e}')
                        return False

            except Exception as e:
                logger.console.error(f'An exception occurred while opening the yaml dir: {e}')
                return False
        return True
