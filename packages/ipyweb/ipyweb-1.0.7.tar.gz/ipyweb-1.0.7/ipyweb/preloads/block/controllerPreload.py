from ipyweb.app import app
from ipyweb.module import module
from ipyweb.logger import logger
from ipyweb.config import config
from ipyweb.service import service
from ipyweb.singleton import singleton
from ipyweb.controller import controller
from ipyweb.contracts.ipywebPreload import ipywebPreload
from ipyweb.contracts.ipywebController import ipywebController


class controllerPreload(ipywebPreload, metaclass=singleton):
    # preload加载此模块时调用的配置信息
    ipywebAutoConfig = {
        'enable': True,  # 是否关闭运行
    }
    controllers = {}

    def run(self, **kwargs):
        self.loadFromControllers(f'ipyweb.{app.controllersName}')
        if config.get('app.autoLoad.loadControllersEnable', True):
            self.loadFromControllers(f'app.{app.controllersName}')
        controller._load(self.controllers)
        return self

    def loadFromControllers(self, path=''):
        try:
            controllerFiles = module.maps(str(path), {})
            if controllerFiles and type(controllerFiles) == dict and len(controllerFiles) > 0:
                for name, spacename in controllerFiles.items():
                    instance = service.get(spacename)
                    if isinstance(instance, ipywebController):  # 必须继承 ipywebController 否则不加载
                        self.controllers[name] = instance
        except Exception as e:
            logger.console.error(f'An exception occurred while reading the controller directory:{e}')
        return self
