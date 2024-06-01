from ipyweb.config import config
class windows():
    ipywebAutoConfig = {
        'enable': config.get('windows.guiDriverEnable',False),  # 是否关闭事件注册器
    }

    def createBefore(self, eventName='', eventRegister=None):
        pass
        # print(f'windowsCreateBefore register ok')

    def created(self, eventName='', eventRegister=None):
        pass
        # print(f'windowsCreated register ok')

    def startBefore(self, eventName='', eventRegister=None):
        pass
        # print(f'windowsStartBefore register ok')

    def started(self, eventName='', eventRegister=None):
        pass
        # print(f'windowsStarted register ok')
