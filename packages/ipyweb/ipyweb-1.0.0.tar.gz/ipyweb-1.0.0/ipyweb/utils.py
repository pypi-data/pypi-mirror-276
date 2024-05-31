import json
import os
import socket
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
    def getFiles(self, **params) -> dict:
        path = params.get('path', '')
        ext = params.get('ext', '.py')
        replaceExt = params.get('replaceExt', True)
        appendFileName = params.get('appendFileName', False)
        format = params.get('format', True)
        formatSep = params.get('formatSep', '.')
        result = {}
        try:
            for root, dirs, files in os.walk(os.path.normpath(path)):
                if '__pycache__' in dirs: dirs.remove('__pycache__')
                for file in files:
                    if file.endswith(ext):
                        file_path = os.path.join(root, file)

                        if format:
                            file_path = file_path.replace(os.sep, formatSep)
                        if replaceExt:
                            file_path = file_path.replace(ext, '')
                            file_name = file_path.split('.')[-1]
                        else:
                            file_name = file_path.split('.')[-2]
                        if appendFileName:
                            file_path += formatSep + file_name
                        result[file_name] = file_path
        except Exception as e:
            pass

        return result

    @classmethod
    def checkUrl(self, domain, port) -> bool:
        try:
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
    def closePort(self, port):
        pid = 0
        try:
            process_info = self.findProcessByPort(port)
            if process_info:
                pid = process_info['pid']
                self.killPid(pid)
        except Exception as e:
            pass
        return pid

    @classmethod
    def killPid(self, pid, myself=False):
        try:
            if os.getpid() != pid or (myself == True and os.getpid() == pid):
                os.kill(pid, 9)
        except OSError:
            pass

    @classmethod
    def findProcessByPort(self, port):
        import psutil
        for proc in psutil.process_iter(['pid', 'name']):
            for conn in proc.connections():
                if conn.laddr[1] == port:
                    return proc.info
        return None

    @classmethod
    def isPort(self, port, host='127.0.0.1') -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((host, port))
                return True
            except ConnectionRefusedError:
                return False

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
