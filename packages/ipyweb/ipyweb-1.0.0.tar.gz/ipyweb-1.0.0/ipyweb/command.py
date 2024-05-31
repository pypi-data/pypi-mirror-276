import os
import click
import importlib.util
from ipyweb.app import app
from ipyweb.config import config
from ipyweb.utils import utils
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
        if self._loaded == True:
            return self
        if self.isPyInstaller() == False:
            click.echo(f'please install PyInstaller...')
            return self
        self._loadFromDir(f'./{app.ipywebPath}/{app.commandsName}')
        if config.get('app.autoLoad.loadCommandsEnable', True):
            self._loadFromDir(f'./{app.appPath}/{app.getName()}/{app.backendName}/{app.commandsName}')
        self._loaded = True
        return self

    @classmethod
    def isPyInstaller(self):

        try:
            import PyInstaller
            return True
        except ImportError:
            return False

    @classmethod
    def _loadFromDir(self, dir=''):
        try:
            files = utils.getFiles(path=os.path.normpath(dir))
            if files and type(files) == dict and len(files) > 0:
                for name, path in files.items():
                    self._loadFromModule(name, os.path.normpath('./' + path.replace('.', '/') + '.py'))
        except Exception as e:
            click.echo(f'加载命令目录异常:{e}')

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
            click.echo(f'载入命令异常:{e}')

        return self
