import os
import click
import importlib.util
from ipyweb.app import app, appIpyweb
from ipyweb.config import config
from ipyweb.singleton import singleton


class command(metaclass=singleton):
    @classmethod
    def load(self):
        commandIpyweb._load()
        return self

    @classmethod
    def getCommands(self):
        return commandIpyweb._commands


class commandIpyweb(metaclass=singleton):
    _commands = {}
    _loaded = False

    @classmethod
    def _load(self):
        if appIpyweb._loaded == False: appIpyweb.load()

        if self._loaded == True:
            return self
        self._loadFromDir(f'{app.ipywebPath}/{app.commandsName}')
        if config.get('app.autoLoad.loadCommandsEnable', True):
            for appName in self._getAppNames():
                self._loadFromDir(f'{app.appPath}/{appName}/{app.backendName}/{app.commandsName}')
        self._loaded = True
        return self

    @classmethod
    def _getAppNames(self):
        absmpath = app.path(f'{app.rootPath}/{app.appPath}')
        if not os.path.isdir(absmpath):
            return []
        contents = os.listdir(absmpath)
        apps = [d for d in contents if os.path.isdir(os.path.join(absmpath, d))]
        if '__pycache__' in apps: apps.remove('__pycache__')
        return apps

    @classmethod
    def _loadFromDir(self, dir=''):
        try:
            files = self.getFiles(path=dir, format=False, replaceExt=False)
            if files and type(files) == dict and len(files) > 0:
                for name, path in files.items():
                    self._loadFromModule(name, path)
        except Exception as e:
            click.echo(f'An exception occurred while reading the command directory:{e}')

    @classmethod
    def _loadFromModule(self, moduleName='', modulePath=''):
        try:
            spec = importlib.util.spec_from_file_location(moduleName, modulePath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if module:
                for name, cmd in vars(module).items():
                    if isinstance(cmd, click.Command):  self._commands.update({name: cmd})
            if hasattr(module, moduleName):
                moduleInstance = getattr(module, moduleName)
                for name, cmd in vars(moduleInstance).items():
                    if isinstance(cmd, click.Command):  self._commands.update({name: cmd})

        except Exception as e:
            click.echo(f'An exception occurred while reading the command module:{e}')

        return self

    @classmethod
    def getFiles(self, **params) -> dict:
        path = params.get('path', '')
        ext = params.get('ext', '.py')
        result = {}
        if path.startswith(app.ipywebPath):
            rootPrefix = app.ipywebRootPath
        else:
            rootPrefix = app.rootPath
        absmpath = app.path(f'{rootPrefix}/{path}')

        try:
            for root, dirs, files in os.walk(absmpath):
                if '__pycache__' in dirs: dirs.remove('__pycache__')
                for file in files:
                    if file.endswith(ext):
                        file_path = os.path.join(root, file)
                        file_name = os.path.basename(file_path).replace(ext, '')
                        result[file_name] = file_path
        except Exception as e:
            click.echo(f'An exception occurred while reading the command dirs:{e}')

        return result
