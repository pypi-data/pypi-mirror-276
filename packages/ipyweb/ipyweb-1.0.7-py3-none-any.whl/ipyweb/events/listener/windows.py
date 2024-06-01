from ipyweb.config import config

class windows():
    ipywebAutoConfig = {
        'enable': config.get('windows.guiDriverEnable', False),  # 是否关闭事件监听
    }

    def windows_createBefore(self, winCls, **kwargs):
        pass

    def windows_created(self, winCls, **kwargs):
        pass

    def windows_startBefore(self, winCls, **kwargs):
        pass

    def windows_started(self, winCls, **kwargs):
        pass
