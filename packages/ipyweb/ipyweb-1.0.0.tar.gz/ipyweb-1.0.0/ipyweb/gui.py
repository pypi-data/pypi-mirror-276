from ipyweb.app import appIpyweb
from ipyweb.config import config, configIpyweb
from ipyweb.logger import loggerIpyweb
from ipyweb.singleton import singleton


class gui:
    guiDriver = None


class guiIpyweb(metaclass=singleton):
    _loaded = False
    _guiDriver = None

    @classmethod
    def load(self, reload=False):
        if appIpyweb._loaded == False: appIpyweb.load()
        if loggerIpyweb._loaded == False: loggerIpyweb.load()
        if configIpyweb._loaded == False: configIpyweb.load()

        if config.get('windows.guiDriverEnable', True) == False and reload == False:
            return None
        if self._loaded == False or reload == True:
            guiDriver = config.get('windows.guiDriver', '')
            guiConfig = config.get(f'windows.guiDriverConfig.{guiDriver}', {})
            if guiDriver == 'remote':
                from ipyweb.guis.RemoteServer import RemoteServer
                self._guiDriver = RemoteServer(guiConfig).run()
            elif guiDriver == 'local':
                from ipyweb.guis.LocalServer import LocalServer
                self._guiDriver = LocalServer(guiConfig).run()
            elif guiDriver == 'flask':
                from ipyweb.guis.FlaskServer import FlaskServer
                self._guiDriver = FlaskServer(guiConfig).run()
            elif guiDriver == 'ipyweb':
                from ipyweb.guis.IpywebServer import IpywebServer
                self._guiDriver = IpywebServer(guiConfig).run()
            else:
                from ipyweb.guis.BottleServer import BottleServer
                self._guiDriver = BottleServer(guiConfig).run()

        return self._guiDriver
