from ipyweb.app import app
from ipyweb.logger import logger
from ipyweb.config import config as sysConfig


class db():
    database = None
    config = None

    def __init__(self, connects='', **config):
        self.config = dict(self._parseConnects(connects), **config)

    def open(self, connects='', **config):
        self.config = dict(self._parseConnects(connects), **config)
        if self.database is None:
            self.database = dbIpyweb(**self.config).open()
        return self.database

    def _parseConnects(self, connects=''):
        result = {}
        cs = []
        if '.' in connects:
            cs = connects.split('.')
        if len(cs) >= 1:
            result['driver'] = cs[0]
        if len(cs) >= 2:
            result['connect'] = cs[1]
        return result


class dbIpyweb():
    _config = {}
    _connect = ''
    _driver = ''
    _database = None
    _driverParams = {}
    _defaultConnect = 'default'
    _defaultDriver = 'sqlite'

    def __init__(self, **kwargs):
        self.load(**kwargs)

    def load(self, **kwargs):
        try:
            from peewee import SqliteDatabase
        except ImportError:
            logger.console.error('please installer the module: peewee (pip install peewee)')
            return self

        self._setConfig(kwargs.get('config', {}))._setDriver(kwargs.get('driver', ''))._setConnect(
            kwargs.get('connect', ''))._setDriverParams(kwargs.get('driverParams', {}))
        return self

    def open(self, **kwargs):
        try:
            self.load(**kwargs)
            if self._driver not in ['sqlite', 'mysql', 'postgresql']:
                logger.console.error(f'Unsupported database driver [{self._driver}]')
                return self._database
            if len(self._driverParams) <= 0:
                logger.console.error(f'The database configuration information does not exist')
                return self._database

            self._driverParams['database'] = app.path(f'{app.realResourcesPath}/{self._driverParams["database"]}')

            if self._driver == 'mysql':
                from playhouse.pool import PooledMySQLDatabase
                self._database = PooledMySQLDatabase(**self._driverParams)
            elif self._driver == 'postgresql':
                from playhouse.pool import PostgresqlDatabase
                self._database = PostgresqlDatabase(**self._driverParams)
            else:
                from peewee import SqliteDatabase
                self._database = SqliteDatabase(**self._driverParams)
        except Exception as e:
            logger.console.error(f'An exception occurred while database initialization ：{e}')
        return self._database

    def _setConfig(self, config={}):
        try:
            self._config = dict(self._config, **sysConfig.get('database', {}))
            if type(config) == dict and len(config) > 0:
                self._config = dict(self._config, **config)
        except Exception as e:
            logger.console.error(f'An exception occurred while retrieving database configuration：{e}')
        if type(self._config) == dict and len(self._config) <= 0:
            logger.console.error(f'Failed to retrieve database configuration')
        return self

    def _setConnect(self, connect=''):
        try:
            self._connect = connect if connect else self._connect
            if self._connect == '':
                self._connect = self._config.get(f'{self._driver}.connect', self._defaultConnect)
        except Exception as e:
            logger.console.error(f'An exception occurred while retrieving the database connection name：{e}')
        return self

    def _setDriver(self, dirver=''):
        try:
            self._driver = dirver if dirver else self._driver
            if self._driver == '':
                self._driver = self._config.get('defaultDriver', self._defaultDriver)
        except Exception as e:
            logger.console.error(f'An exception occurred while retrieving the database driver name：{e}')

        return self

    def _setDriverParams(self, driverParams={}):
        try:
            self._driverParams = self._config.get(self._driver, {}).get(self._connect, {})
            if type(driverParams) == dict and len(driverParams) > 0:
                self._driverParams = dict(self._driverParams, **driverParams)
        except Exception as e:
            logger.console.error(f'An exception occurred while retrieving the database driver configuration：{e}')
        return self
