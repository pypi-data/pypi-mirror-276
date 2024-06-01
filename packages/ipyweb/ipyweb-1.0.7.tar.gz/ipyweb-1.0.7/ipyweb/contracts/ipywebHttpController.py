from ipyweb.utils import utils
from ipyweb.logger import logger
from ipyweb.controller import controller
from ipyweb.singleton import singleton


class ipywebHttpController(metaclass=singleton):
    if utils.isModuleInstalled('flask'):
        try:
            from flask import Blueprint
            blueprint = Blueprint('app', __name__)
        except ImportError:
            logger.console.error('flask is not installed')

    def __init__(self):
        if hasattr(self, 'registerRoute'): self.registerRoute()

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
