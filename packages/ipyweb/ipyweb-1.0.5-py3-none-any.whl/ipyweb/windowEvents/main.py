import multiprocessing
from ipyweb.appRunner import appRunner
from ipyweb.process import process
from ipyweb.logger import logger


class main:
    def killPid(self, event=''):
        try:
            for name, proc in process.getProcesses().items():
                process.kill(proc.get('pid'))
                logger.console.debug(f'[{event}]]关闭进程[{name}] [PID:{proc.get("pid")}]')
            active_processes = multiprocessing.active_children()
            for proc in active_processes:
                process.kill(proc.pid)
                logger.console.debug(f'[{event}]]关闭子进程[{proc.name}] [PID:{proc.pid}]')
        except Exception as e:
            logger.console.error(f'[{event}]关闭已建进程异常:{e}')
        return self

    def onClosed(self):
        try:
            appRunnerModule, appRunnerCls = appRunner.load()
            if hasattr(appRunnerCls, 'onClosed'):
                onClosed = getattr(appRunnerCls, 'onClosed')
                if callable(onClosed): onClosed()
        except Exception as e:
            logger.console.error(f'窗口关闭事件回调异常:{e}')

        return self

    def closed(self, window, *args, **kwargs):
        self.killPid('closed')
        self.onClosed()

    def closing(self, window, *args, **kwargs):
        self.killPid('closing')

    def shown(self, window, *args, **kwargs):
        pass
        # window.expose(echo,test)
        # logger.console.debug('shown')

    def loaded(self, window, *args, **kwargs):
        pass
        # logger.console.debug('loaded')

    def minimized(self, window, *args, **kwargs):
        pass
        # logger.console.debug('minimized')

    def maximized(self, window, *args, **kwargs):
        pass
        # logger.console.debugint('maximized')

    def restored(self, window, *args, **kwargs):
        pass
        # logger.console.debug('restored')

    def resized(self, window, *args, **kwargs):
        pass
        # logger.console.debug('resized')

    def moved(self, window, *args, **kwargs):
        pass
        # logger.console.debug('moved')
