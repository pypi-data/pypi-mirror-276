from ipyweb.singleton import singleton
from ipyweb.contracts.ipywebPreload import ipywebPreload
from ipyweb.process import processIpyweb


class processPreload(ipywebPreload, metaclass=singleton):
    # preload加载此模块时调用的配置信息
    ipywebAutoConfig = {
        'enable': True,  # 是否关闭运行
    }

    def run(self, **kwargs):
        processIpyweb.load()
        return self
