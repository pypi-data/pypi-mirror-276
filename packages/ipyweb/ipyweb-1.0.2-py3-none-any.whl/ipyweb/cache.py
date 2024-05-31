from functools import lru_cache
from ipyweb.app import app, appIpyweb
from ipyweb.contracts.ipywebException import ipywebException
from ipyweb.logger import loggerIpyweb, logger
from ipyweb.singleton import singleton
from ipyweb.config import config as sysConfig, configIpyweb


class cache():
    diskcache = None

    def __init__(self, **kwargs):
        self.diskcache = cacheIpyweb.load(False, **kwargs)

    def __getattr__(self, name):
        if hasattr(self.diskcache, name) != True:
            return self.diskcache
        methods = getattr(self.diskcache, name, None)
        return methods if callable(methods) else self.diskcache


class cacheIpyweb(metaclass=singleton):
    _diskcache = None
    _loaded = False
    _config = {
        'path': 'diskcache'
    }
    _connect = ''
    _driver = ''
    _driverParams = {}
    _defaultConnect = 'default'
    _defaultDriver = 'diskcache'

    def __init__(self, **kwargs):
        self.load(**kwargs)

    @classmethod
    @lru_cache(128)
    def load(self, reload=False, **kwargs):
        if appIpyweb._loaded == False: appIpyweb.load()
        if loggerIpyweb._loaded == False: loggerIpyweb.load()
        if configIpyweb._loaded == False: configIpyweb.load()
        if sysConfig.get('app.autoLoad.isLoadCache', True) == False and reload == False:
            return None
        if self._loaded == False or reload == True:

            try:
                from diskcache import Cache as DiskCache
            except ImportError:
                logger.console.error('please installer the module: diskcache (pip install diskcache)')
                return None

            self._setConfig(kwargs.get('config', {}))._setDriver(kwargs.get('driver', ''))._setConnect(
                kwargs.get('connect', ''))._setDriverParams(kwargs.get('driverParams', {}))._open()
            if app.lifecycleDebug:
                print('::::::::::::::::::::::::::cache loaded::::::::::::::::::::::::::')
            self._loaded = True
        return self._diskcache

    def reload(self, **kwargs):
        return self.load(True, **kwargs)

    @classmethod
    def _open(self):
        try:
            if self._driver not in ['diskcache']:
                logger.console.error(f'Unsupported database cache [{self._driver}]')
                return self._diskcache
            if self._driver == 'diskcache':
                from diskcache import Cache as DiskCache
                self._diskcache = DiskCache(
                    app.path(f'{app.runtimePath}/{self._driverParams.get("path", self._config.get("path", ""))}'),
                    **self._driverParams)

        except Exception as e:
            ipywebException(f'An exception occurred while cache initialization ：{e}')
        return self._diskcache

    @classmethod
    def _setConfig(self, config={}):
        try:
            self._config = dict(self._config, **sysConfig.get('cache', {}))
            if type(config) == dict and len(config) > 0:
                self._config = dict(self._config, **config)
        except Exception as e:
            logger.console.error(f'An exception occurred while retrieving datcacheabase configuration：{e}')
        if type(self._config) == dict and len(self._config) <= 0:
            logger.console.error(f'Failed to retrieve cache configuration')
        return self

    @classmethod
    def _setConnect(self, connect=''):
        try:
            self._connect = connect if connect else self._connect
            if self._connect == '':
                self._connect = self._config.get(f'{self._driver}.connect', self._defaultConnect)
        except Exception as e:
            logger.console.error(f'An exception occurred while retrieving the cache connection name：{e}')
        return self

    @classmethod
    def _setDriver(self, dirver=''):
        try:
            self._driver = dirver if dirver else self._driver
            if self._driver == '':
                self._driver = self._config.get('defaultDriver', self._defaultDriver)
        except Exception as e:
            logger.console.error(f'An exception occurred while retrieving the cache driver name：{e}')

        return self

    @classmethod
    def _setDriverParams(self, driverParams={}):
        try:
            self._driverParams = self._config.get(self._driver, {}).get(self._connect, {})
            if type(driverParams) == dict and len(driverParams) > 0:
                self._driverParams = dict(self._driverParams, **driverParams)
        except Exception as e:
            logger.console.error(f'An exception occurred while retrieving the cache driver configuration：{e}')
        return self
