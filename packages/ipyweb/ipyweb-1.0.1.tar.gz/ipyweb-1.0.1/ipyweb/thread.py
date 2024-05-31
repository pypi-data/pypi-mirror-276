import os
import pickle
import threading
from concurrent.futures import ThreadPoolExecutor
from ipyweb.logger import logger
from ipyweb.singleton import singleton


class thread(metaclass=singleton):

    @classmethod
    def get(self, name=''):
        return threadIpyweb.threads.get('name') if name else threadIpyweb.threads

    @classmethod
    def run(self, **params):
        return threadIpyweb._run(**params)

    @classmethod
    def runPool(self, **params):
        return threadIpyweb._runPool(**params)


class threadIpyweb(metaclass=singleton):
    threads = {}

    @classmethod
    def _target(self, **params):
        appTarget = params.get('target', None)
        if callable(appTarget):
            config = {
                'name': params.get('name', ''),
                'config': params.get('config', {}),
                'pid': os.getpid(),
            }
            try:
                appTarget(**config)
            except TypeError as e:
                appTarget()
        return self

    @classmethod
    def _runPool(self, **params):
        name = params.get('name', 'default')
        target = params.get('target', None)
        config = params.get('config', {})
        onStart = params.get('onStart', None)
        onError = params.get('onError', None)

        if target is None or callable(target) == False:
            return None
        try:
            if self.threads.get(name, None) is None:
                self.threads[name] = {}
                self.threads[name]['params'] = params
                if config.get('block', False):  # 阻塞运行

                    with ThreadPoolExecutor(max_workers=config.get('max', 1), thread_name_prefix=name) as executor:
                        self.threads[name]['thread'] = executor = executor.submit(
                            self._target,
                            **params  # 不要使用kwargs形式赋值**config 为了保持回调一致 这里不要改成 kwargs=config
                        )
                        # result = executor.result()
                        # done=executor.done()
                else:  # 非阻塞运行
                    self.threads[name]['thread'] = executor = ThreadPoolExecutor(
                        max_workers=config.get('max', 1),
                        thread_name_prefix=name
                    )
                    try:
                        self.threads[name]['thread'] = executor.submit(
                            self._target,
                            **params  # 不要使用kwargs形式赋值**config 为了保持回调一致 这里不要改成 kwargs=config
                        )
                    finally:
                        pass
                        # executor.shutdown()  # 参数True形成阻塞 非阻塞可自行关闭线程池
                if callable(onStart): onStart(executor)

            return executor
        except pickle.PicklingError as e:
            msg = f'A serialization error occurred while starting the [{name}] thread pool.'
            logger.console.error(msg)
            if callable(onError): onError(msg, e)
        except Exception as e:
            msg = f'An exception occurred while starting with the [{name}] thread pool:{e}'
            logger.console.error(msg)
            if callable(onError): onError(msg, e)

        return None

    @classmethod
    def _run(self, **params):
        params = params
        name = params.get('name', 'default')
        target = params.get('target', None)
        config = params.get('config', {})
        onStart = params.get('onStart', None)
        onError = params.get('onError', None)
        if target is None or callable(target) == False:
            return None
        try:
            if self.threads.get(name, None) is None:
                self.threads[name] = {}
                self.threads[name]['params'] = params
                self.threads[name]['thread'] = threading.Thread(
                    name=name,
                    target=self._target,
                    kwargs=params
                )
                self.threads[name]['thread'].daemon = config.get('daemon', True)
                self.threads[name]['thread'].start()
                if config.get('block', False):  # 是否阻塞
                    self.threads[name]['thread'].join()
                if callable(onStart): onStart(self.threads[name]['thread'])
            return self.threads[name]['thread']
        except pickle.PicklingError as e:
            msg = f'A serialization error occurred while starting the [{name}] thread.'
            logger.console.error(msg)
            if callable(onError): onError(msg, e)
        except Exception as e:
            msg = f'An exception occurred while starting with the [{name}] thread:{e}'
            logger.console.error(msg)
            if callable(onError): onError(msg, e)
        return None
