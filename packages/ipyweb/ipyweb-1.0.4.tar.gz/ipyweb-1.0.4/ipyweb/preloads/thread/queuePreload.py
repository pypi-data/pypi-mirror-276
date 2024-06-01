from ipyweb.app import app
from ipyweb.config import config
from ipyweb.logger import logger
from ipyweb.service import service
from ipyweb.contracts.ipywebPreload import ipywebPreload
from ipyweb.services.queue import queue, queueRunner


class queuePreload(ipywebPreload):
    # preload加载此模块时调用的配置信息
    ipywebAutoConfig = {
        'enable': True,  # 是否关闭运行
        'daemon': True,  # 是否守护执行
        'block': False,  # 是否阻塞执行
        'max': 1,  # 进程池或线程池数量
        'usePool': False,  # 是否线程池
    }
    queues = {}

    def run(self, **kwargs):
        self.load()
        return self

    def load(self):
        self._loadFromQueques(f'{app.ipywebPath}.{app.queuesName}')
        if config.get('app.autoLoad.loadQuequesEnable', False) == True:
            self._loadFromQueques(f'{app.appPath}.{app.queuesName}')
        try:
            for name, module in self.queues.items():
                moduleConfig = getattr(module, app.ipywebAutoConfigName, {})
                if moduleConfig.get('enable', False) == True: self.quequeRun(name, moduleConfig, module)
        except Exception as e:
            logger.console.error(f'An exception occurred while reading the queue dirs:{e}')
        return self

    def _loadFromQueques(self, path=''):
        try:
            modules = service.module(path)
            for name, module in modules.items():
                self.queues[name] = module
        except Exception as e:
            logger.console.error(f'An exception occurred while reading the queue module:{e}')
        return self

    def quequeRun(self, name='', moduleConfig={}, quequeModule=None):
        try:
            config = dict(moduleConfig, **{
                'name': quequeModule.__module__,
                'run': moduleConfig.get('run', quequeModule.run if hasattr(quequeModule, 'run') else None),
                'onStart': moduleConfig.get('onStart',
                                            quequeModule.onStart if hasattr(quequeModule, 'onStart') else None),
                'onRecv': moduleConfig.get(
                    'onRecv',
                    quequeModule.onRecv if hasattr(quequeModule, 'onRecv') else None),

                'onEmpty': moduleConfig.get('onEmpty',
                                            quequeModule.onEmpty if hasattr(quequeModule, 'onEmpty') else None),
                'onFull': moduleConfig.get('onFull', quequeModule.onFull if hasattr(quequeModule, 'onFull') else None),
                'onError': moduleConfig.get('onError',
                                            quequeModule.onError if hasattr(quequeModule, 'onError') else None),
            })

            queueRunner().run(**config)
        except Exception as e:
            logger.console.error(f'An exception occurred while starting the queue module [{name}]:{e}')
        return self
