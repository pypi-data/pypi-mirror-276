import os
import re
from pathlib import Path
from ipyweb.ipyweb import ipyweb
from ipyweb.app import app
from ipyweb.config import config
from ipyweb.logger import logger
from ipyweb.module import module
from ipyweb.utils import utils


class builder():
    hiddenImports = []
    cmds = []
    _name = ''
    _appPath = ''
    _bulidPath = ''
    _config = {
        'pyinstallerCmd': []
    }

    @classmethod
    def run(self, name=''):

        app.setName(name)  # 动态设置应用名称
        self._name = app.getName()
        ipyweb.bootBaser(True)
        self._appPath = f'./{app.appPath}/{self._name}'
        self._config = dict(self._config, **config.get('build', []))
        self._bulidPath = f'./{app.bulidPathName}/{self._name}'
        console = 'console' if config.get('app.debug', False) == True else 'noconsole'
        distpath = self._getNormpath(f'{self._bulidPath}/dist')
        workpath = self._getNormpath(f'{self._bulidPath}/src')
        hooks = self._getNormpath(f'./ipyweb/builds/hooks')
        specpath = self._getNormpath(self._bulidPath)
        self.cmds = [
            'run.py',
            f'--name={self._name}',  # 自定义生成的可执行文件名称
            f'--{console}',  # 是否显示控制台
            f'--onedir',  # 生成单一可执行文件 onedir onefile 单文件启动相对较慢 单文件启动时需要解压目录到临时文件夹  建议文件夹生成安装包
            f'--noconfirm',  # 无需用户确认
            f'--distpath={distpath}',  # 编译目录
            f'--workpath={workpath}',  # 源文件目录
            f'--specpath={specpath}',  # 指定spec目录
        ]

        includeDirName = self._isIncludeDirName()
        if includeDirName:
            self.cmds += [f'--contents-directory={includeDirName}']  # 单独文件存放编译目录 pyinstaller6.0.以上支持
        if config.get('windows.gui', '') == 'cef':
            self.cmds += [f'--additional-hooks-dir={hooks}']  # 钩子文件目录  本项目必须目录内钩子
            self.cmds += [f'--hidden-import=cefpython3']
        else:
            self.cmds += [f'--exclude-module=cefpython3']

        if config.get('windows.gui', '') == 'qt':
            self.cmds += [f'--hidden-import=qtpy']
            self.cmds += [f'--hidden-import=pyside2']
        else:
            self.cmds += [f'--exclude-module=qtpy']
            self.cmds += [f'--exclude-module=pyside2']

        if config.get('windows.url', '') == '':
            self.cmds += [f'--hidden-import=pywebview']  # 缓存模块
        else:
            self.cmds += [f'--exclude-module=pywebview']
        if config.get('app.autoLoad.isLoadCache', True):
            self.cmds += [f'--hidden-import=diskcache']  # 缓存模块
        else:
            self.cmds += [f'--exclude-module=diskcache']

        if config.get('app.autoLoad.isLoadEvent', True):
            self.cmds += [f'--hidden-import=blinker']  # 事件模块
        else:
            self.cmds += [f'--exclude-module=blinker']
        if config.get('app.autoLoad.isLoadORM', True):
            self.cmds += [f'--hidden-import=peewee']  # ORM模块
        else:
            self.cmds += [f'--exclude-module=peewee']

        # 设置图标参数
        self._setIco()
        # 拷贝资源目录
        self._copyDirFiles(f'{self._appPath}/{app.resourcesName}')
        # 动态导入的模块
        hiddenimports = self.getHiddenImports(True)
        self.cmds += hiddenimports
        # 追加应用配置
        for cmd in self._config.get('cmds', []):
            self.cmds.append(cmd)
        return self

    @classmethod
    def _isIncludeDirName(self):
        try:
            import PyInstaller
            version = PyInstaller.__version__
            match = re.search(r"^\d+\.\d+(\.\d+)?", version)
            if match.group(0) >= "6.0.0":
                return '_' + self._name
        except Exception as e:
            pass

        return ''

    @classmethod
    def getCmds(self):
        return self.cmds

    @classmethod
    def clear(self):
        try:

            realDistpath, realName = self._getRealRealPath()
            if realDistpath and realName and config.get('windows.gui', '') == 'cef':
                libcef = os.path.normpath(f'{realDistpath}/{realName}/cefpython3/libcef.dll')
                if os.path.exists(libcef): os.remove(libcef)  # py3.7-py3.9该文件导致异常
        except Exception as e:
            logger.console.error(f'An exception occurred during cleanup after successful build: {e}')
        return self

    @classmethod
    def _setIco(self):
        ico = '/assets/logo.ico'
        if os.path.exists(f'{self._appPath}/{app.resourcesName}{ico}'):
            path = os.path.abspath(f'{self._appPath}/{app.resourcesName}/{ico}')
            self.cmds.append(f'--icon={path}')  # 指定图标文件路径
        return self

    @classmethod
    # 拷贝资源文件所有文件目录
    def _copyDirFiles(self, dir=''):
        try:
            copyFiles = []
            for dir in self._getSubDir(self._getNormpath(dir)):
                targetSubDir = dir.split(os.sep)[:-1]
                sourcePath = os.path.abspath(f'{self._appPath}/{app.resourcesName}/{dir}')
                targetPath = f'{app.resourcesName}{os.sep}{os.sep.join(targetSubDir)}'
                if utils.os() == 'win':
                    path = f'{sourcePath};{targetPath}'
                else:
                    path = f'{sourcePath}:{targetPath}'
                copyFiles.append(f'--add-data={self._getNormpath(path)}')
            for cmd in copyFiles:
                self.cmds.append(cmd)
        except Exception as e:
            pass

        return self

    @classmethod
    def _getSubDir(self, directory=''):
        subdirectories = []
        try:
            subdirectories = [str(x).replace(directory, '') for x in Path(directory).rglob('*') if
                              x.is_file()]
        except Exception as e:
            pass

        return subdirectories

    @classmethod
    def _getNormpath(self, path=''):
        return os.path.normpath(path)

    @classmethod
    def _getRealRealPath(self):
        realDistpath = ''
        realName = ''
        try:
            for cmd in self.cmds:
                if cmd.startswith('--distpath'):
                    realDistpath = cmd.split('=')[1]
                if cmd.startswith('--name'):
                    realName = cmd.split('=')[1]

            includeDirName = self._isIncludeDirName()
            if includeDirName:
                realName = realName + '/' + includeDirName

        except Exception as e:
            pass
        return realDistpath, realName

    @classmethod
    def getHiddenImports(self, prefix=False):
        self.hiddenImports = []
        try:
            for mod in module.modules(True):
                prefix = '--hidden-import=' if prefix else ''
                self.hiddenImports.append(prefix + mod)
        except Exception as e:
            logger.console.error(f'An exception occurred while importing the dynamic module: {e}')

        return self.hiddenImports
