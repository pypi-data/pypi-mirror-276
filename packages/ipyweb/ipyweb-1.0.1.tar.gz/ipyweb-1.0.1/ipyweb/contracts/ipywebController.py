

from ipyweb.singleton import singleton
from ipyweb.controller import controller


class ipywebController(metaclass=singleton):

    @classmethod
    def windows(self, name=''):
        return controller._getWindows(name)

    @classmethod
    def error(self, msg='error', data={}, code=1):
        return self.json(code, msg, data)

    @classmethod
    def success(self, msg='success', data={}):
        return self.json(0, msg, data)

    @classmethod
    def json(self, code=0, msg='success', data={}):
        return {
            'code': code,
            'message': msg,
            'data': data
        }
