from ipyweb.preload import preload
from ipyweb.singleton import singleton
from ipyweb.contracts.ipywebRunner import ipywebRunner


class ipywebPreload(ipywebRunner, metaclass=singleton):
    preload = preload()

    def getProcess(self):
        return preload.getProcess()

    def getThread(self):
        return preload.getThread()

    def getBlock(self):
        return preload.getBlock()
