from ipyweb.app import app, appIpyweb
from ipyweb.config import config, configIpyweb
from ipyweb.service import service
from ipyweb.singleton import singleton
from ipyweb.logger import logger, loggerIpyweb
from ipyweb.thread import thread
from ipyweb.process import process


class preload(metaclass=singleton):

    @classmethod
    def getBlock(self, name=''):
        return preloadIpyweb.blocks.get(name, None) if name else preloadIpyweb.blocks

    @classmethod
    def getThread(self, name=''):
        return preloadIpyweb.threads.get(name, None) if name else preloadIpyweb.threads

    @classmethod
    def getProcess(self, name=''):
        return preloadIpyweb.processes.get(name, None) if name else preloadIpyweb.processes


class preloadIpyweb(metaclass=singleton):
    _loaded = False
    ipyweb = None
    blocks = {}
    threads = {}
    processes = {}
    preloadBlocks = {}
    preloadThreads = {}
    preloadProcesss = {}

    @classmethod
    def load(self, reload=False):

        if self._loaded == True and reload == True:
            return self

        if appIpyweb._loaded == False: appIpyweb.load()
        if loggerIpyweb._loaded == False: loggerIpyweb.load()
        if configIpyweb._loaded == False: configIpyweb.load()

        self._loadFromPreloadBlocks(f'{app.ipywebPath}.{app.preloadsName}/block')
        self._loadFromPreloadThreads(f'{app.ipywebPath}.{app.preloadsName}/thread')
        self._loadFromPreloadProcess(f'{app.ipywebPath}.{app.preloadsName}/process')

        if config.get('app.autoLoad.loadPrelodsEnable', True):
            self._loadFromPreloadBlocks(f'{app.appPath}.{app.preloadsName}/block')
            self._loadFromPreloadThreads(f'{app.appPath}.{app.preloadsName}/thread')
            self._loadFromPreloadProcess(f'{app.appPath}.{app.preloadsName}/process')
        for name, module in self.preloadBlocks.items():
            self._runBlock(name, module)
        for name, module in self.preloadThreads.items():
            self._runThread(name, module)
        for name, module in self.preloadProcesss.items():
            self._runProcess(name, module)
        if app.lifecycleDebug:
            print('::::::::::::::::::::::::::preload loaded::::::::::::::::::::::::::')
        self._loaded = True

        return self

    @classmethod
    def reload(self):
        self.load(True)
        return self

    @classmethod
    def _loadFromPreloadBlocks(self, path=''):
        try:
            modules = service.module(path)
            for name, module in modules.items():
                self.preloadBlocks[name] = module
        except Exception as e:
            logger.console.error(f'An exception occurred while parsing the blocking preloader:{e}')
        return self

    @classmethod
    def _loadFromPreloadThreads(self, path=''):
        try:
            modules = service.module(path)
            for name, module in modules.items():
                self.preloadThreads[name] = module
        except Exception as e:
            logger.console.error(f'An exception occurred while parsing the thread preloader:{e}')
        return self

    @classmethod
    def _loadFromPreloadProcess(self, path=''):
        try:
            modules = service.module(path)
            for name, module in modules.items():
                self.preloadProcesss[name] = module
        except Exception as e:
            logger.console.error(f'An exception occurred while parsing the process preloader:{e}')
        return self

    @classmethod
    def _runBlock(self, name='', module=None):
        try:
            moduleConfig = getattr(module, app.ipywebAutoConfigName, {})
            if moduleConfig.get('enable', False) != True:
                return self
            if hasattr(module, 'run'):
                self.blocks[name] = module.run
                module.run()
        except Exception as e:
            logger.console.error(f'[{name}]An exception occurred while executing the blocking preloader:{e}')
        return self

    @classmethod
    def _runThread(self, name='', module=None):
        try:
            if self.threads.get(name, None) is None:
                moduleConfig = getattr(module, app.ipywebAutoConfigName, {})
                usePool = moduleConfig.get('usePool', False)
                if moduleConfig.get('enable', False) != True:
                    return self
                threadName = moduleConfig.get('name', '')
                threadName = threadName if threadName else module.__module__
                if usePool == True:
                    self.threads[name] = thread.runPool(
                        name=threadName,
                        target=module.run if hasattr(module, 'run') else None,
                        onStart=module.onStart if hasattr(module, 'onStart') else None,
                        onError=module.onError if hasattr(module, 'onError') else None,
                        config={
                            'max': moduleConfig.get('max', 1),
                            'daemon': moduleConfig.get('daemon', True),
                            'block': moduleConfig.get('block', False),
                        })
                else:
                    self.threads[name] = thread.run(
                        name=threadName,
                        target=module.run if hasattr(module, 'run') else None,
                        onStart=module.onStart if hasattr(module, 'onStart') else None,
                        onError=module.onError if hasattr(module, 'onError') else None,
                        config={
                            'max': moduleConfig.get('max', 1),
                            'daemon': moduleConfig.get('daemon', True),
                            'block': moduleConfig.get('block', False),
                        })

        except Exception as e:
            logger.console.error(f'An exception occurred while executing the thread preloader:{e}')
        return self

    @classmethod
    def _runProcess(self, name='', module=None):

        try:
            if self.processes.get(name, None) is None:
                moduleConfig = getattr(module, app.ipywebAutoConfigName, {})
                usePool = moduleConfig.get('usePool', False)

                if moduleConfig.get('enable', False) != True:
                    return self
                processName = moduleConfig.get('name', '')
                processName = processName if processName else module.__module__
                if usePool == True:
                    self.processes[name] = process.runPool(
                        name=processName,
                        target=module.run,
                        onStart=module.onStart if hasattr(module, 'onStart') else None,
                        onError=module.onError if hasattr(module, 'onError') else None,
                        onMessage=module.onMessage if hasattr(module, 'onMessage') else None,
                        onIpc=module.onIpc if hasattr(module, 'onIpc') else None,
                        onShare=module.onShare if hasattr(module, 'onShare') else None,
                        config={
                            'max': moduleConfig.get('max', 1),
                            'daemon': moduleConfig.get('daemon', True),
                            'block': moduleConfig.get('block', False),
                            'reloadIpyweb': moduleConfig.get('reloadIpyweb', True),
                        })
                else:

                    self.processes[name] = process.run(
                        name=processName,
                        target=module.run,
                        onStart=module.onStart if hasattr(module, 'onStart') else None,
                        onError=module.onError if hasattr(module, 'onError') else None,
                        onMessage=module.onMessage if hasattr(module, 'onMessage') else None,
                        onIpc=module.onIpc if hasattr(module, 'onIpc') else None,
                        onShare=module.onShare if hasattr(module, 'onShare') else None,
                        config={
                            'max': moduleConfig.get('max', 1),
                            'daemon': moduleConfig.get('daemon', True),
                            'block': moduleConfig.get('block', False),
                            'reloadIpyweb': moduleConfig.get('reloadIpyweb', True),
                        })

        except Exception as e:
            logger.console.error(f'An exception occurred while executing the process preloader:{e}')
        return self
