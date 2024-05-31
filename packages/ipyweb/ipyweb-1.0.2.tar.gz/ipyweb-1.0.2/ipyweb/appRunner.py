import sys
import time
import importlib
from ipyweb.app import app, appIpyweb
from ipyweb.utils import utils
from ipyweb.config import config, configIpyweb
from ipyweb.logger import logger, loggerIpyweb
from ipyweb.singleton import singleton
from ipyweb.pywebview.windows import windows


class appRunner(metaclass=singleton):
    appRunnerDefaultName = 'runner'
    appRunnerDefaultClsName = 'runner'
    appRunnerDefaultAction = 'run'
    appRunner = None
    appRunnerCls = None
    onWindowsOpened = None
    appName = ''
    _loaded = False

    @classmethod
    def boot(self):
        try:
            if self.load():

                if hasattr(self.appRunnerCls, self.appRunnerDefaultAction):
                    run = getattr(self.appRunnerCls, self.appRunnerDefaultAction)

                    if config.get('windows.guiDriverEnable', True):
                        windows().run({},
                                      onStarted=self._onStarted,
                                      onCreated=self._onCreated,
                                      onCreateBefore=self._onCreateBefore,
                                      onStartBefore=self._onStartBefore
                                      )
                    else:
                        if callable(self.onWindowsOpened): self.onWindowsOpened(self.appName)
                        run(None)
                        try:
                            while True:
                                time.sleep(3600 * 24 * 30)
                        except KeyboardInterrupt as e:
                            logger.console.debug(f"The application [{self.appName}] has exited normally.")

        except Exception as e:
            logger.console.error(f'An exception occurred during application [{self.appName}]  startup: {e}')
            time.sleep(3)
            sys.exit(0)

        return self

    @classmethod
    def load(self, reload=False):
        if self._loaded == False or reload == True:
            if appIpyweb._loaded == False: appIpyweb.load()
            if loggerIpyweb._loaded == False: loggerIpyweb.load()
            if configIpyweb._loaded == False: configIpyweb.load()
            self.getAppRunner()
            self.getAppRunnerCls()
            self._loaded = True
        return self.appRunner, self.appRunnerCls

    @classmethod
    def getAppRunner(self):
        self.appName = config.moduleMaps('name',
                                         app.getName()) if app.isExe else app.getName()  # 编译后读取module应用名 非编译环境直接读取
        appModulePath = '.'.join([app.appPath, self.appName, self.appRunnerDefaultName])
        try:
            self.appRunner = utils.smartImportModule(self.appRunnerDefaultName, appModulePath, app.rootPath)
        except ModuleNotFoundError as e:
            logger.console.error(f'The application startup module does not exist:[{appModulePath}]')
        except Exception as e:
            logger.console.error(f'An exception occurred while retrieving the startup module:[{appModulePath}]')
        return self.appRunner

    @classmethod
    def getAppRunnerCls(self):
        try:
            if self.appRunner:
                appRunnerClsAttr = getattr(self.appRunner, self.appRunnerDefaultClsName)
                self.appRunnerCls = appRunnerClsAttr()
        except Exception as e:
            logger.console.error(
                f'An exception occurred while retrieving an instance of the application [{self.appName}] startup module: {e}')
            time.sleep(3)
            sys.exit(0)
        return self.appRunnerCls

    @classmethod
    def _onCreateBefore(self, winCls=None):
        if hasattr(self.appRunnerCls, 'onCreateBefore') and callable(self.appRunnerCls.onCreateBefore):
            self.appRunnerCls.onCreateBefore()

    @classmethod
    def _onStartBefore(self, winCls=None):

        if hasattr(self.appRunnerCls, 'onStartBefore') and callable(self.appRunnerCls.onStartBefore):
            self.appRunnerCls.onStartBefore(winCls)

    @classmethod
    def _onCreated(self, winCls=None):

        if hasattr(self.appRunnerCls, 'onCreated') and callable(self.appRunnerCls.onCreated):
            self.appRunnerCls.onCreated(winCls)

    @classmethod
    def _onStarted(self, winCls):
        if callable(self.onWindowsOpened): self.onWindowsOpened(self.appName)
        if hasattr(self.appRunnerCls, 'run') and callable(
                self.appRunnerCls.run) and winCls.windows: self.appRunnerCls.run(winCls.windows)

    @classmethod
    def setOnWindowsOpened(self, onWindowsOpened=None):
        self.onWindowsOpened = onWindowsOpened
        return self
