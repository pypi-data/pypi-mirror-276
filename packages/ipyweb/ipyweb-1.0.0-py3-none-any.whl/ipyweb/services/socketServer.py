import asyncio
import os
from ipyweb.logger import logger
from ipyweb.process import process
from ipyweb.thread import thread
from ipyweb.utils import utils


class socketServer():

    def run(self, *args, **params):
        # pool版携带参数嵌套kwargs
        params = params.get('kwargs', {}) if params.get('kwargs', None) is not None else params
        return socketServerIpyweb()._run(**params)


class socketServerIpyweb():
    websockets = set()
    websocket = None
    path = ''
    name = ''
    config = {
        'host': 'localhost',
        'port': 8765
    }
    _logUseTxt = ''

    def _run(self, **params):
        self.name = params.get("name", "")
        self.config = dict(self.config, **params.get('config'))
        useProcess = '进程' if self.config.get("useProcess", True) else '线程'
        usePool = '池' if self.config.get("usePool", True) else ''
        self._logUseTxt = f'{useProcess}{usePool}'
        if self.config.get('autoKill', True): self._autoKillPort()
        asyncio.run(self._start())
        return self

    async def _runServe(self):

        import websockets

        serveConfig = dict(self.config.get('serveConfig', {}), **{
            'ws_handler': lambda wss, path: self._onMessage(wss, path),
            'host': self.config.get('host'),
            'port': self.config.get('port'),
        })
        if self.config.get('ssl', False) and self.config.get('serveConfig', {}).get('ssl', None) is None:
            import ssl
            from webview import generate_ssl_cert
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            keyfile, certfile = generate_ssl_cert()
            ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)
            serveConfig['ssl'] = ssl_context

        async with websockets.serve(**serveConfig) as server:
            logger().console.debug(
                f'[{self.name}][ws://{self.config.get("host")}:{self.config.get("port")}]使用{self._logUseTxt}启动成功[PID:{os.getpid()}]')
            onReady = self.config.get('onReady', None)
            if callable(onReady): await onReady(server)
            await server.wait_closed()

    async def _start(self):

        try:
            await  self._runServe()
        except OSError as e:
            if e.errno == 10048 and self.config.get('autoKill', True):
                logger().console.debug(f'[{self.name}]socket使用{self._logUseTxt}端口被占用')
                self._autoKillPort()
                await self._runServe()
            else:
                logger().console.error(f'[{self.name}]socket使用{self._logUseTxt}系统异常:{e}')
            onError = self.config.get('onError', None)
            if callable(onError): await onError(e)
        except Exception as e:
            logger().console.error(f'[{self.name}]socket使用{self._logUseTxt}启动异常:{e}')
            onError = self.config.get('onError', None)
            if callable(onError): await onError(e)

    async def _onMessage(self, websocket, path):
        self.websockets.add(websocket)
        if self.websocket is None:
            onConnect = self.config.get('onConnect', None)
            if callable(onConnect): await onConnect(websocket, path)
        self.websocket = websocket
        self.path = path
        onMessage = self.config.get('onMessage', None)
        import websockets
        try:
            async for message in self.websocket:
                try:
                    if callable(onMessage): await onMessage(message)
                except Exception as e:
                    onError = self.config.get('onError', None)
                    if callable(onError):
                        await onError(e)
        # except websockets.ConnectionClosed as e:
        #     print(f"Connection closed: {e.code} {e.reason}")
        #     self.websocket = None
        #     self.path = ''
        #     onClosed = self.config.get('onClosed', None)
        #     if callable(onClosed): await onClosed()
        except Exception as e:
            onError = self.config.get('onError', None)
            if callable(onError): await onError(e)
        finally:
            self.websocket = None
            self.path = ''
            self.websockets.remove(websocket)
            onClosed = self.config.get('onClosed', None)
            if callable(onClosed): await onClosed()



    def _autoKillPort(self):
        try:
            port = self.config.get('port')
            if port and utils.isPort(port) and self.config.get('autoKill', True):
                utils.closePort(port)
        except Exception as ex:
            pass
        return self


class socketServerRunner():

    def run(self, **config):
        """
             config = {
                'name':'socket',#定时器名称 名称不能重复 否则以已存在的名称运行
                'daemon': True,  # 是否守护执行
                'block': False,  # 是否阻塞执行
                'max': 1,  # 进程池或线程池数量
                'useProcess': False,  # 是否使用独立进程 默认独立线程
                'usePool': True,  # 是否线程池或进程池,
                'onReady': onReady, #准备连接
                'onConnect':onConnect, #连接成功回调
                'onError': onError,#错误回调
                'onClosed': onClosed,#关闭回调
                'onMessage': onMessage#消息回调
             }
               """

        try:
            useProcess = config.get('useProcess', False)
            usePool = config.get('usePool', False)
            params = dict({
                'name': config.get('name', __name__),
                'target': socketServer().run,
                'config': config
            })

            if useProcess:
                (process.runPool if usePool else process.run)(**params)
            else:
                (thread.runPool if usePool else thread.run)(**params)

        except Exception as e:
            logger.console.error(f'socket服务启动异常:{e}')
