from ipyweb.app import app
from ipyweb.config import config
from ipyweb.contracts.ipywebPreload import ipywebPreload
from ipyweb.logger import logger
from ipyweb.service import service
from ipyweb.services.timer import timer


class timerPreload(ipywebPreload):
    timers = {}
    ipywebAutoConfig = {
        'enable': True,  # 是否关闭运行
        'daemon': True,  # 是否守护执行
        'block': False,  # 是否阻塞执行
        'max': 1,  # 进程池或线程池数量
        'usePool': True,  # 是否线程池或进程池
    }

    def run(self, **config):
        self.load()

    def load(self):
        self._loadFromTimesDir(f'{app.ipywebPath}.{app.timersName}')
        if config.get('app.autoLoad.loadTimersEnable', False) == True:
            self._loadFromTimesDir(f'{app.appPath}.{app.timersName}')
        try:

            for name, module in self.timers.items():
                moduleConfig = getattr(module, app.ipywebAutoConfigName, {})
                if moduleConfig.get('enable', False) == True: self.timerRun(name, moduleConfig, module)
        except Exception as e:
            logger.console.error(f'An exception occurred while reading the timer dirs:{e}')
        return self

    def _loadFromTimesDir(self, dirs=''):

        try:
            modules = service.module(dirs)

            for name, module in modules.items():
                self.timers[name] = module
        except Exception as e:
            logger.console.error(f'An exception occurred while reading the timer module:{e}')
        return self

    def timerRun(self, name, moduleConfig, module):
        try:
            moduleConfig['run'] = module.run if hasattr(module, 'run') else None
            moduleConfig['onStart'] = module.onStart if hasattr(module, 'onStart') else None
            moduleConfig['onError'] = module.onError if hasattr(module, 'onError') else None
            moduleConfig['name'] = moduleConfig.get('name', module.__module__)
            timer().run(**moduleConfig)
        except Exception as e:
            logger.console.error(f'An exception occurred while starting the timer module :{e}')
        return self
