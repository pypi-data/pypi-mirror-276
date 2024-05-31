import os
import pickle
import time
import multiprocessing

from ipyweb.app import appIpyweb, app
from ipyweb.config import configIpyweb
from ipyweb.event import event, eventIpyweb
from ipyweb.logger import logger, loggerIpyweb
from ipyweb.module import moduleIpyweb
from ipyweb.singleton import singleton
from ipyweb.thread import thread
from ipyweb.utils import utils


class process(metaclass=singleton):
    @classmethod
    def getProcesses(self):
        return processIpyweb.processes

    @classmethod
    def runPool(self, **params):
        return processIpyweb._runPool(**params)

    @classmethod
    def run(self, **params):
        return processIpyweb._run(**params)

    @classmethod
    def send(self, message):
        return processIpyweb._send(message)

    @classmethod
    def listen(self, name='', onMessage=None):
        return processIpyweb._listen(name, onMessage)


class processIpyweb(metaclass=singleton):
    processes = {}
    _loaded = False
    _pipes = {}

    @classmethod
    def load(self, reload=False):
        if self._loaded == False or reload == True:
            self._loaded = True
        return self

    @classmethod
    def reload(self):
        self._loaded = False
        return self.load(True)

    @classmethod
    def _send(self, message):
        name = message.get('name', '')
        if name in self._pipes and self._pipes[name].get('main', None):
            self._pipes[name]['main'].send(message)
            return True
        return False

    @classmethod
    def _listen(self, name='', onMessage=None):
        if name in self._pipes and self._pipes[name].get('main', None):
            mainPipe = self._pipes[name]['main']
            thread.run(
                name=__name__ + '.' + name,
                target=self._mainPipeOnRecv,
                config={
                    'mainPipe': mainPipe,
                    'onMessage': onMessage
                }
            )
            self._pipes[name]['listening'] = True

    @classmethod
    def _ipywebBootBaser(self, name=''):
        app.setName(name)
        appIpyweb.load(True)
        loggerIpyweb.load(True)
        configIpyweb.load(True)
        moduleIpyweb.load(True)
        eventIpyweb.load(True)
        return self

    @classmethod
    def _target(self, appName, childPipe, shareData, **params):
        if params.get('config', {}).get('reloadIpyweb', True): self._ipywebBootBaser(appName)
        appTarget = params.get('target', None)
        if callable(appTarget) != True:
            return self
        config = {
            'name': params.get('name', ''),
            'config': params.get('config', {}),
            'pid': os.getpid(),
            'share': shareData
        }
        name = params.get('name', 'default')
        onIpc = params.get('onIpc', None)
        onMessage = params.get('onMessage', None)
        if callable(onIpc): onIpc(childPipe)
        try:
            if callable(appTarget): appTarget(**config)
        except TypeError as e:
            if callable(appTarget): appTarget()

        if onIpc and callable(onIpc) and childPipe and callable(onMessage):
            thread.run(
                name=__name__ + '.' + name,
                target=self._childPipeOnRecv,
                config={
                    'childPipe': childPipe,
                    'onMessage': onMessage
                }
            )

    @classmethod
    def _mainPipeOnRecv(self, **params):
        mainPipe = params.get('config', {}).get('mainPipe', None)
        onMessage = params.get('config', {}).get('onMessage', None)
        while callable(onMessage) and mainPipe:
            try:
                data = mainPipe.recv()
                if data and callable(onMessage):
                    onRecv = data.get('onRecv', None)
                    result = onMessage(data.get('message', None))
                    if callable(onRecv): onRecv(result)
                time.sleep(3)
            except KeyboardInterrupt as e:
                pass
            except Exception as e:
                pass

    @classmethod
    def _childPipeOnRecv(self, **params):

        childPipe = params.get('config', {}).get('childPipe', None)
        onMessage = params.get('config', {}).get('onMessage', None)

        while callable(onMessage) and childPipe:
            try:
                data = childPipe.recv()
                if data == None:
                    childPipe.close()
                if data and callable(onMessage):
                    onRecv = data.get('onRecv', None)
                    result = onMessage(data.get('message', None))
                    if callable(onRecv): onRecv(result)
                time.sleep(3)
            except KeyboardInterrupt as e:
                pass
            except Exception as e:
                pass

    @classmethod
    def _runPool(self, **params):
        name = params.get('name', 'default')
        target = params.get('target', None)
        onIpc = params.get('onIpc', None)
        onShare = params.get('onShare', None)
        onStart = params.get('onStart', None)
        onError = params.get('onError', None)
        poolConfig = params.get('poolConfig', {})
        config = params.get('config', {})
        if target is None or callable(target) == False:
            return None
        try:

            if self.processes.get(name, None) is None:
                mainPipe = None
                childPipe = None
                if onIpc and callable(onIpc):
                    mainPipe, childPipe = multiprocessing.Pipe()
                    self._pipes[name] = {
                        'main': mainPipe,
                        'child': childPipe,
                        'listening': False,  # 主进程是否监听中
                    }
                self.processes[name] = {}
                self.processes[name]['params'] = params
                if utils.isWin(): multiprocessing.freeze_support()
                poolConfig = dict({
                    'processes': config.get('max', 1)
                }, **poolConfig)
                with multiprocessing.Manager() as manager:
                    shareData = onShare(manager) if callable(onShare) else None
                    if config.get('block', False):  # 阻塞运行
                        self.processes[name]['pool'] = pool = multiprocessing.Pool(**poolConfig).apply(
                            func=self._target,
                            args=(app.getName(), childPipe, shareData,),
                            kwds=params
                        )
                    else:  # 非阻塞运行
                        self.processes[name]['pool'] = pool = multiprocessing.Pool(**poolConfig).apply_async(
                            func=self._target,
                            args=(app.getName(), childPipe, shareData,),
                            kwds=params
                        )
                        # pool.close()
                        # pool.join()
                    self.processes[name]['pid'] = 0
                    if callable(onStart): onStart(self.processes[name]['pool'])

            return self.processes[name]['pool']
        except pickle.PicklingError as e:
            msg = f'A serialization error occurred while starting the [{name}] process pool.'
            logger.console.error(msg)
            if callable(onError): onError(msg, e)
        except Exception as e:
            msg = f'An exception occurred while starting with the [{name}] process pool:{e}'
            logger.console.error(msg)
            if callable(onError): onError(msg, e)
        return None

    @classmethod
    def _run(self, **params):

        name = params.get('name', 'default')
        target = params.get('target', None)
        onIpc = params.get('onIpc', None)
        onShare = params.get('onShare', None)
        onStart = params.get('onStart', None)
        onError = params.get('onError', None)
        config = params.get('config', {})
        if target is None or callable(target) == False:
            return None

        try:
            if self.processes.get(name, None) is None:
                if utils.isWin(): multiprocessing.freeze_support()
                mainPipe = None
                childPipe = None
                if onIpc and callable(onIpc):
                    mainPipe, childPipe = multiprocessing.Pipe()
                    self._pipes[name] = {
                        'main': mainPipe,
                        'child': childPipe,
                        'listening': False,  # 主进程是否监听中
                    }
                with multiprocessing.Manager() as manager:
                    shareData = onShare(manager) if callable(onShare) else None
                    self.processes[name] = {}
                    self.processes[name]['params'] = params
                    self.processes[name]['process'] = multiprocessing.Process(
                        name=name,
                        target=self._target,
                        args=(app.getName(), childPipe, shareData,),
                        kwargs=params,
                    )

                    self.processes[name]['process'].daemon = config.get('daemon', True)
                    self.processes[name]['process'].start()
                    if config.get('block', False):  # 是否阻塞
                        self.processes[name]['process'].join()
                    self.processes[name]['pid'] = self.processes[name]['process'].pid
                    if callable(onStart): onStart(self.processes[name]['process'])
            return self.processes[name]['process']


        except pickle.PicklingError as e:
            msg = f'A serialization error occurred while starting the [{name}] process.'
            logger.console.error(msg)
            if callable(onError): onError(msg, e)
        except Exception as e:
            msg = f'An exception occurred while starting with the [{name}] process:{e}'
            logger.console.error(msg)
            if callable(onError): onError(msg, e)
        return None
