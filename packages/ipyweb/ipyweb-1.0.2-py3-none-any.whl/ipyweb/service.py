import importlib
from ipyweb.app import app
from ipyweb.utils import utils
from ipyweb.logger import logger
from ipyweb.singleton import singleton
from ipyweb.module import module as moduleMap


class service(metaclass=singleton):
    @classmethod
    def ipyweb(self, invokeCls='', *args, **kwargs):
        return serviceIpyweb._loadClass(f'{app.ipywebPath}.{invokeCls}', *args, **kwargs)

    @classmethod
    def controller(self, invokeCls='', *args, **kwargs):
        return serviceIpyweb._loadClass(invokeCls, app.controllersName, *args, **kwargs)

    @classmethod
    def preload(self, invokeCls='', *args, **kwargs):
        return serviceIpyweb._loadClass(invokeCls, app.preloadsName, *args, **kwargs)

    @classmethod
    def addon(self, invokeCls='', *args, **kwargs):
        return serviceIpyweb._loadClass(invokeCls, app.addonsName, *args, **kwargs)

    @classmethod
    def socket(self, invokeCls='', *args, **kwargs):
        return serviceIpyweb._loadClass(invokeCls, app.socketsName, *args, **kwargs)

    @classmethod
    def queue(self, invokeCls='', *args, **kwargs):
        return serviceIpyweb._loadClass(invokeCls, app.queuesName, *args, **kwargs)

    @classmethod
    def get(self, invokeCls='', *args, **kwargs):
        return serviceIpyweb._loadClass(invokeCls, app.servicesName, *args, **kwargs)

    @classmethod
    def module(self, path='', instance=True, loadClass=True, *args, **kwargs):
        return serviceIpyweb._module(path, instance, loadClass, *args, **kwargs)


class serviceIpyweb(metaclass=singleton):

    @classmethod
    def _loadClass(self, invokeCls='', spaceName=app.servicesName, *args, **kwargs):
        try:
            prerix = f'{app.appPath}.{app.getName()}.{app.backendName}'
            className = ''
            if len(invokeCls.split('.')) == 1:
                invokeCls = f'{prerix}.{spaceName}.{invokeCls}'
            if len(invokeCls.split('.')) == 2:
                tempCls = invokeCls.split('.')
                invokeCls = f'{prerix}.{spaceName}.{tempCls[0]}'
                className = tempCls[1]

            className = className if className else invokeCls.split('.')[-1]
            rootPrefix = app.ipywebRootPath if invokeCls.startswith(app.ipywebPath) else app.rootPath
            classModule = utils.smartImportModule(className, invokeCls, rootPrefix)

            if hasattr(classModule, className):
                classAttr = getattr(classModule, className)
                classInstance = classAttr(*args, **kwargs)
                return classInstance
            else:
                logger.console.error(
                    f' The name [{className}] of the instantiated service class [{invokeCls}] is incorrect')
        except ImportError as e:
            logger.console.error(f'The instantiated service class [{str(invokeCls)}] does not exist')
        except Exception as e:
            logger.console.error(f'An exception occurred while instantiating the service class [{invokeCls}] : {e}')
        return None

    @classmethod
    def _loadModule(self, invokeCls='', spaceName=app.servicesName):
        try:
            prerix = f'{app.appPath}.{app.getName()}.{app.backendName}'
            if len(invokeCls.split('.')) == 1:
                invokeCls = f'{prerix}.{spaceName}.{invokeCls}'
            className = invokeCls.split('.')[-1]
            rootPrefix = app.ipywebRootPath if invokeCls.startswith(app.ipywebPath) else app.rootPath
            classModule = utils.smartImportModule(className, invokeCls, rootPrefix)
            return classModule
        except Exception as e:
            logger.console.error(f'An exception occurred while instantiating the class [{invokeCls}]: {e}')
        return None

    @classmethod
    def _module(self, path='', instance=True, loadClass=True, *args, **kwargs):
        modules = {}
        try:

            moduleFiles = moduleMap.jsonFileMaps(str(path), {})
            if moduleFiles and type(moduleFiles) == dict and len(moduleFiles) > 0:
                for name, module in moduleFiles.items():
                    if loadClass:
                        modules[name] = self._loadClass(module, '', *args, **kwargs) if instance else module
                    else:
                        modules[name] = self._loadModule(module, *args, **kwargs) if instance else module
        except ImportError as e:
            logger.console.error(f'Module [{str(path)}] does not exist')
        except Exception as e:
            logger.console.error(f'An exception occurred while loading the dynamic module:{e}')
        return modules
