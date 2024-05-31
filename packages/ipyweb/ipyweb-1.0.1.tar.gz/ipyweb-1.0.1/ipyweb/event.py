from ipyweb.app import appIpyweb, app
from ipyweb.config import configIpyweb, config
from ipyweb.logger import loggerIpyweb, logger
from ipyweb.service import service
from ipyweb.singleton import singleton


class event(metaclass=singleton):

    def __init__(self):
        eventIpyweb.load()

    @classmethod
    def emit(self, eventName='', *args, **kwargs):
        return eventIpyweb._emit(eventName, *args, **kwargs)

    @classmethod
    def register(self, eventName='', eventFn=None):
        return eventIpyweb._userRegister(eventName, eventFn)

    @classmethod
    def on(self, eventName='', eventListener=None):
        return eventIpyweb._on(eventName, eventListener)

    @classmethod
    def once(self, eventName='', eventListener=None):
        return eventIpyweb._once(eventName, eventListener)

    @classmethod
    def off(self, eventName=''):
        return eventIpyweb._off(eventName)

    @classmethod
    def delete(self, eventName=''):
        return eventIpyweb._delete(eventName)

    @classmethod
    def has(self, eventName=''):
        return eventIpyweb._has(eventName)

    @classmethod
    def reOn(self, eventName=''):
        return eventIpyweb._reOn(eventName)

    @classmethod
    def isRun(self, eventName=''):
        return eventIpyweb._isRun(eventName)


class eventIpyweb(metaclass=singleton):
    _loaded = False
    _events = {}
    _registers = {}
    _listeners = {}

    def __init__(self):
        self.load()

    @classmethod
    def load(self, reload=False):

        if self._loaded == True and reload == True:
            return self
        if appIpyweb._loaded == False: appIpyweb.load()
        if loggerIpyweb._loaded == False: loggerIpyweb.load()
        if configIpyweb._loaded == False: configIpyweb.load()
        if config.get('app.autoLoad.isLoadEvent', True) == False and reload == False:
            return None

        self._loadFromEventRegisters(f'{app.ipywebPath}.{app.eventsName}/register')
        self._loadFromEventListeners(f'{app.ipywebPath}.{app.eventsName}/listener')
        if config.get('app.autoLoad.loadEventsEnable', True):
            self._loadFromEventRegisters(f'{app.appPath}.{app.eventsName}/register')
            self._loadFromEventListeners(f'{app.appPath}.{app.eventsName}/listener')
        if app.lifecycleDebug:
            print('::::::::::::::::::::::::::event loaded::::::::::::::::::::::::::')
        self._loaded = True

    @classmethod
    def _loadFromEventListeners(self, path=''):
        try:
            self._listeners = service.module(path)

            if len(self._listeners) > 0:
                for className, module in self._listeners.items():
                    moduleConfig = getattr(module, app.ipywebAutoConfigName, {})
                    if moduleConfig.get('enable', False) == True: self._sysListener(module)
        except Exception as e:
            logger.console.error(f'An exception occurred while loading event listeners:{e}')
        return self

    @classmethod
    def _loadFromEventRegisters(self, path=''):

        try:
            self._registers = service.module(path)

            for className, module in self._registers.items():
                moduleConfig = getattr(module, app.ipywebAutoConfigName, {})
                if moduleConfig.get('enable', False) == True: self._sysRegister(className, module)
        except Exception as e:
            logger.console.error(f'An exception occurred while  loading event registers:{e}')
        return self

    @classmethod
    def _sysListener(self, module=None):
        try:
            classAttrs = dir(module)
            classMethods = [
                attr for attr in classAttrs if
                callable(getattr(module, attr)) and not attr.startswith('__') and not attr.endswith('__')
            ]
            for method in classMethods:
                if self._has(method):
                    eventFn = getattr(module, method)
                    eventId = id(eventFn)
                    if eventId not in self._events[method]['listener']:
                        self._events[method]['listener'][eventId] = eventFn
                        self._events[method]['register'].connect(eventFn)
                        self._events[method]['running'] = True
        except Exception as e:
            logger.console.error(f'An exception occurred while executing the event listeners:{e}')
        return self

    @classmethod
    def _sysRegister(self, className='', module=None):
        try:
            from blinker import signal
            classMethods = self._getClassMethods(module)
            for method in classMethods:
                eventName = f'{className}_{method}'
                eventFn = getattr(module, method)
                if self._has(eventName) == False:
                    self._events[eventName] = {}
                    self._events[eventName]['register'] = signal(eventName)
                    self._events[eventName]['listener'] = {}
                    self._events[eventName]['running'] = True
                    self._events[eventName]['repeat'] = True
                    self._events[eventName]['count'] = 0
                    try:
                        eventFn(eventName, self._events[eventName]['register'])
                    except TypeError as e:
                        eventFn()

        except Exception as e:
            logger.console.debug(f'An exception occurred while executing the event registers: {e}')

        return self

    @classmethod
    def _userRegister(self, eventName='', eventFn=None):
        result = False
        try:
            from blinker import signal
            if self._has(eventName) == False:
                self._events[eventName] = {}
                self._events[eventName]['register'] = signal(eventName)
                self._events[eventName]['listener'] = {}
                self._events[eventName]['running'] = True
                self._events[eventName]['repeat'] = True
                self._events[eventName]['count'] = 0
                result = True
            if callable(eventFn):
                try:
                    eventFn(eventName, self._events[eventName]['register'])
                except TypeError as e:
                    eventFn()

        except Exception as e:
            logger.console.debug(f'An exception occurred while registering an event [{eventName}] : {e}')
        return result

    @classmethod
    def _once(self, eventName='', eventListener=None):
        result = False
        try:
            if self._has(eventName) and callable(eventListener):
                eventId = id(eventListener)
                self._events[eventName]['listener'][eventId] = eventListener
                self._events[eventName]['register'].connect(eventListener)
                self._events[eventName]['repeat'] = False
                self._events[eventName]['count'] = 0  # 置空 再次监听仍然可以监听一次
                result = True
        except Exception as e:
            logger.console.debug(f'An exception occurred while subscribing to the once event [{eventName}] : {e}')
        return result

    @classmethod
    def _on(self, eventName='', eventListener=None):
        result = False
        try:
            if self._has(eventName) and callable(eventListener):
                eventId = id(eventListener)
                self._events[eventName]['listener'][eventId] = eventListener
                self._events[eventName]['register'].connect(eventListener)
                result = True
        except Exception as e:
            logger.console.debug(f'An exception occurred while subscribing to the event [{eventName}] : {e}')
        return result

    @classmethod
    def _off(self, eventName=''):
        result = False
        try:
            if self._has(eventName):
                self._events[eventName]['running'] = False
                result = True
        except Exception as e:
            logger.console.debug(f'An exception occurred while closing the event [{eventName}] : {e}')
        return result

    @classmethod
    def _reOn(self, eventName=''):
        result = False
        try:
            if self._has(eventName):
                self._events[eventName]['running'] = True
                result = True
        except Exception as e:
            logger.console.debug(f'An exception occurred while restarting the event [{eventName}] : {e}')
        return result

    @classmethod
    def _has(self, eventName):
        return True if eventName in self._events else False

    @classmethod
    def _isRun(self, eventName):
        return True if self._has(eventName) and self._events[eventName].get('running', None) == True else False

    @classmethod
    def _emit(self, eventName, *args, **kwargs):
        result = False
        try:
            if self._has(eventName) and self._events[eventName].get('running', None) == True:
                self._events[eventName]['register'].send(*args, **kwargs)
                self._events[eventName]['count'] = self._events[eventName]['count'] + 1
                # 仅监听一次
                if self._events[eventName].get('repeat', None) == False and self._events[eventName]['count'] >= 1:
                    self._events[eventName]['running'] = False

            result = True
        except Exception as e:
            logger.console.debug(f'An exception occurred while emiting the event [{eventName}] : {e}')
        return result

    @classmethod
    def _delete(self, eventName=''):
        result = False
        try:
            if self._has(eventName):
                del self._events[eventName]
                result = True
        except Exception as e:
            logger.console.debug(f'An exception occurred while deleting the event [{eventName}] : {e}')
        return result

    @classmethod
    def _getClassMethods(self, module=None):
        if module is None:
            return []
        classMethods = []
        try:
            classAttrs = dir(module)
            classMethods = [
                attr for attr in classAttrs if
                callable(getattr(module, attr)) and not attr.startswith('__') and not attr.endswith('__')
            ]
        except Exception as e:
            pass
        return classMethods
