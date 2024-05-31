import time
from ipyweb.logger import logger
from ipyweb.process import process
from ipyweb.thread import thread


class timer():
    running = False
    defaultInterval = 1
    defaultSleepTime = 0

    def run(self, **config):
        timerRunner().run(**config)
        return self

    def stop(self):
        self.running = False
        return self

    def start(self, **config):

        config = config.get('config', {})
        run = config.get('run', None)
        onStart = config.get('onStart', None)
        onError = config.get('onError', None)
        try:
            self.running = True
            if callable(onStart): onStart(self)
            time.sleep(config.get('sleep', self.defaultSleepTime))
            while self.running == True and callable(run):
                try:
                    run(self)
                except TypeError as e:
                    run()
                time.sleep(config.get('interval', self.defaultInterval))
        except KeyboardInterrupt as e:
            pass
        except Exception as e:
            logger.console.debug(f"An exception occurred while executing the timer:{e}")
            if callable(onError): onError(e)
        return self


# 智能启动
class timerRunner():

    def run(self, **config):
        """
       config = {
        'name':__name__,#定时器名称 名称不能重复 否则以已存在的名称运行
        'run':run,#回调执行方法
        'daemon': True,  # 是否守护执行
        'block': False,  # 是否阻塞执行
        'max': 1,  # 进程池或线程池数量
        'useProcess': False,  # 是否使用独立进程 默认独立线程
        'usePool': False,  # 是否线程池或进程池
        'interval': 5,  # 间隔时间
        'sleep': 5,  # 延时执行
       }
        """
        try:

            useProcess = config.get('useProcess', False)  # 默认线程
            usePool = config.get('usePool', False)  # 默认进程
            params = {
                'name': config.get('name', __name__),
                'target': self._run,
                'config': config
            }

            if useProcess:
                (process.runPool if usePool else process.run)(**params)
            else:
                (thread.runPool if usePool else thread.run)(**params)

        except Exception as e:
            logger.console.error(f'An exception occurred while starting the timer:{e}')

    def _run(self, **config):
        config = config.get('kwargs', {}) if config.get('kwargs', None) is not None else config
        timer().start(**config)
