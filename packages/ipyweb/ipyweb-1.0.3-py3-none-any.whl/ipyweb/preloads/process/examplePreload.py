from ipyweb.contracts.ipywebPreload import ipywebPreload

class examplePreload(ipywebPreload):
    # preload加载此模块时调用的配置信息
    ipywebAutoConfig = {
        'enable': False,  # 是否关闭运行
        'daemon': True,  # 是否守护执行
        'block': False,  # 是否阻塞执行
        'max': 1,  # 进程池数量
        'usePool': False,  # 是否使用进程池
    }
    queues = {}

    def run(self, **kwargs):
        return self
