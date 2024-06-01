import json
import os
from json import JSONDecodeError
from ipyweb.app import app, appIpyweb
from ipyweb.logger import logger, loggerIpyweb
from ipyweb.config import config, configIpyweb
from ipyweb.singleton import singleton


class jsonFile():

    def set(self, data={}, filename=''):
        return jsonFileIpyweb.set(data, filename)

    def get(self, filename=''):
        return jsonFileIpyweb.get(filename)


class jsonFileIpyweb(metaclass=singleton):
    _config = {
        'encoding': 'utf-8'
    }
    _loaded = False

    def __init__(self):
        self.load()

    @classmethod
    def load(self):
        if appIpyweb._loaded == False: appIpyweb.load()
        if loggerIpyweb._loaded == False: loggerIpyweb.load()
        if configIpyweb._loaded == False: configIpyweb.load()

    @classmethod
    def set(self, data={}, filename=''):
        try:
            fname = app.path(filename, False)
            with open(fname, 'w', encoding=self.config('encoding')) as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                return True
        except Exception as e:
            logger.file.error(f'An exception occurred while writing to the file [{filename}]:{e}')
        except FileNotFoundError as e:
            logger.file.error(f"The file [{filename}] to write to does not exist")
        except PermissionError:
            logger.file.error(f"No access permission to the file [{filename}]")
        return False

    @classmethod
    def get(self, filename=''):
        try:
            fname = app.path(filename, False)
            if os.path.exists(fname) != True: return {}
            with open(fname, 'r', encoding=self.config('encoding')) as f:
                return json.load(f)
        except Exception as e:
            logger.console.error(f'An exception occurred while reading the file [{filename}]:{e}')
        except JSONDecodeError as e:
            logger.file.error(f"An error occurred while reading the file [{filename}] due to incorrect data format")
        except FileNotFoundError as e:
            logger.file.error(f"The file [{filename}] to read to does not exist")
        except PermissionError:
            logger.file.error(f"No access permission to the file [{filename}]")
        return {}

    @classmethod
    def config(self, name=''):
        self._config = dict(self._config, **config.get('jsonFile.config', {}))
        return self._config[name] if name in self._config else self._config
