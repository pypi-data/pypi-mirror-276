import json
import os
import sys
from urllib.parse import urlparse
from ipyweb.singleton import singleton


class utils(metaclass=singleton):
    def isModuleInstalled(name='') -> bool:
        try:
            import importlib
            importlib.import_module(name)
            return True
        except ImportError:
            return False

    @classmethod
    def pathExists(self, path='') -> bool:
        if os.path.exists(path):
            return True if os.path.isdir(path) else False
        else:
            return False

    @classmethod
    def tuple(self, data=(), index=0, default=None):
        try:
            return data[index]
        except IndexError:
            return default

    @classmethod
    def get(self, data={}, key='', default=None):
        try:
            if key == '':
                return data;
            if '.' in key:
                keys = key.split('.')
                dict = data
                for k in keys:
                    if k in dict:
                        dict = dict.get(k, default)
                    else:
                        return default  # 如果某个键不存在，返回None
                return dict
            else:
                return data.get(key, default)
        except Exception as e:
            return data

    @classmethod
    def checkUrl(self, domain, port) -> bool:
        try:
            import socket
            socket.create_connection((domain, port), timeout=1).close()
            return True
        except socket.error as e:
            return False

    @classmethod
    def getDomainPortByUrl(self, url) -> tuple:
        parsed_url = urlparse(url)
        domain = parsed_url.hostname
        port = parsed_url.port
        if domain == None: domain = 'localhost'
        if port == None: port = 80
        return domain, port

    @classmethod
    def inJson(self, key, json) -> bool:
        return True if key in json else False

    @classmethod
    def isJson(self, strings='') -> bool:
        if isinstance(strings, str):
            try:
                isinstance(int(strings), int)
                return False
            except:
                pass
            try:
                json.loads(strings)
                return True
            except ValueError:
                return False
        else:
            return False

    @classmethod
    def isCls(self, cls=None) -> bool:
        try:
            return True if cls.__class__.name else False
        except Exception:
            return False

    @classmethod
    def isWin(self) -> bool:
        return self.os() == 'win'

    @classmethod
    def os(self) -> str:
        if sys.platform.startswith('win'):
            return 'win'
        elif sys.platform == 'darwin':
            return 'darwin'
        elif sys.platform.startswith('linux'):
            return 'linux'
        else:
            return 'other'

    @classmethod
    def smartImportModule(self, name='', modulePath='', rootPrefix='.'):
        module = None
        import importlib
        try:
            module = importlib.import_module(modulePath)
        except ImportError as e:
            try:
                modulePath = modulePath.replace('.', '/') + '.py'
                modulePath = os.path.normpath(f'{rootPrefix}/{modulePath}')
                spec = importlib.util.spec_from_file_location(name, modulePath)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
            except Exception as e:
                pass
        except Exception as e:
            pass
        return module
