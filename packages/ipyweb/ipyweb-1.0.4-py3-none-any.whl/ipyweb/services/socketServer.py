import os
import asyncio
from ipyweb.logger import logger
from ipyweb.process import process
from ipyweb.thread import thread


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
        useProcess = 'process' if self.config.get("useProcess", True) else 'thread'
        usePool = 'pool' if self.config.get("usePool", True) else ''
        self._logUseTxt = f'{useProcess}{usePool}'
        if self.config.get('autoKill', True): self._autoKillPort()
        asyncio.run(self._start())
        return self

    async def _runServe(self):

        try:
            import websockets
            import psutil
        except ImportError:
            logger.console.error('please installer the module: websockets and psutil (pip install websockets psutil)')
            return self

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
            logger().console.info(
                f'Socket [{self.name}][ws://{self.config.get("host")}:{self.config.get("port")}] use [{self._logUseTxt}] has been started [PID:{os.getpid()}]')
            onReady = self.config.get('onReady', None)
            if callable(onReady): await onReady(server)
            await server.wait_closed()

    async def _start(self):

        try:
            await  self._runServe()
        except OSError as e:
            if e.errno == 10048 and self.config.get('autoKill', True):
                logger().console.debug(f'Socket [{self.name}] port is occupied')
                self._autoKillPort()
                await self._runServe()
            else:
                logger().console.error(
                    f'An exception occurred while killing the socket [{self.name}] process:{e} ')
            onError = self.config.get('onError', None)
            if callable(onError): await onError(e)
        except Exception as e:
            logger().console.error(
                f'An exception occurred while starting the socket [{self.name}] using  {self._logUseTxt}:{e} ')
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
            if port and porter.isPort(port) and self.config.get('autoKill', True):
                porter.closePort(port)
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
            logger.console.error(f'An exception occurred while starting the socket:{e}')


class porter:

    @classmethod
    def closePort(self, port):
        pid = 0
        try:
            process_info = self.findProcessByPort(port)
            if process_info:
                pid = process_info['pid']
                self.killPid(pid)
        except Exception as e:
            pass
        return pid

    @classmethod
    def killPid(self, pid, myself=False):
        try:
            if os.getpid() != pid or (myself == True and os.getpid() == pid):
                os.kill(pid, 9)
        except OSError:
            pass

    @classmethod
    def findProcessByPort(self, port):
        import psutil
        for proc in psutil.process_iter(['pid', 'name']):
            for conn in proc.connections():
                if conn.laddr[1] == port:
                    return proc.info
        return None

    @classmethod
    def isPort(self, port, host='127.0.0.1') -> bool:
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((host, port))
                return True
            except ConnectionRefusedError:
                return False
