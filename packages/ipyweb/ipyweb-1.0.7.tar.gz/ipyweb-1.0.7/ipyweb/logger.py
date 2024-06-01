import logging
import logging.config
import os
import ipyweb.configs.logger as loggerCfg
from ipyweb.app import appIpyweb, app
from ipyweb.singleton import singleton


class logger(metaclass=singleton):
    file = None
    console = None
    logging = None

    def __init__(self):
        if appIpyweb._loaded == False: appIpyweb.load()
        if loggerIpyweb._loaded == False: loggerIpyweb.load()


class loggerIpyweb(metaclass=singleton):
    _loaded = False

    _config = {
        'debug': False,
        'version': 1,
    }
    _handlers = {
        'file': {
            'filename': 'log.log',
        },
        'timFile': {
            'filename': 'log.log',
        }
    }

    @classmethod
    def reload(self):
        self.load(True)
        return self

    @classmethod
    def getConfig(self):
        try:
            loggerCfgData = {name: value for name, value in loggerCfg.__dict__.items() if not name.startswith("_")}
            self._config = dict(self._config, **loggerCfgData)
            os.makedirs(os.path.normpath(app.runtimePath), exist_ok=True)
            self._config['handlers']['file']['filename'] = os.path.normpath(
                f'{app.runtimePath}/{str(self._config.get("handlers", {}).get("file", {}).get("filename", ""))}')
            self._config['handlers']['timFile']['filename'] = os.path.normpath(
                f'{app.runtimePath}/{str(self._config.get("handlers", {}).get("timFile", {}).get("filename", ""))}')
        except Exception as e:
            logging.error(f'An exception occurred while getting config:{e}')
        return self

    @classmethod
    def load(self, reload=False):

        if self._loaded == False or reload == True:
            try:
                self.getConfig()
                logging.config.dictConfig(self._config)
                logger.file = logging.getLogger("fileLogger")
                logger.console = logging.getLogger("consoleLogger")
                logger.logging = logging
                # 日志记录总开关
                if self._config.get('file', False) != True:
                    logger.file = logger.console
                if app.lifecycleDebug:
                    print('::::::::::::::::::::::::::logger loaded::::::::::::::::::::::::::')
                self._loaded = True
            except Exception as e:
                logging.error(f'An exception occurred during the initialization of the log module:{e}')
            return self
