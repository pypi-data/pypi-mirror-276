from ipyweb.app import app
from ipyweb.singleton import singleton
from ipyweb.contracts.ipywebController import ipywebController
from ipyweb.pywebview.windows import windows


class ipyweb(ipywebController, metaclass=singleton):
    def version(self, window, *args):
        try:

            return self.success('获取版本信息成功', {
                'ver': app.ver,
                'version': app.version
            })
        except Exception as e:
            return self.error(f'获取版本信息异常:{e}')

    def create_window(self, window, args):
        try:
            if type(args) != dict:
                return self.error('参数类型不正确')
            args['target'] = True
            if args.get('url', '') == '' and args.get('html', '') == '':
                return self.error('html和url必须设置一个')
            flag = windows().run(args)
            if type(flag) == str:
                return self.error(flag)
            return self.success('打开成功')
        except Exception as e:
            return self.error(f'获取版本信息异常:{e}')

    def set_title(self, window, args):
        try:
            if type(args) == str:
                title = args
            elif type(args) == dict:
                title = args.get('title', '')
            else:
                return self.error('标题不能为空')
            window.set_title(title)
            return self.success('更换窗口标题成功')
        except Exception as e:
            return self.error(f'更换窗口标题异常:{e}')

    def change_url(self, window, args):
        try:
            if type(args) == str:
                url = args
            elif type(args) == dict:
                url = args.get('url', '')
            else:
                return self.error('网址不能为空')
            window.load_url(url)
            return self.success('打开网址成功')
        except Exception as e:
            return self.error(f'打开网址异常:{e}')

    def load_css(self, window, args):
        try:
            if type(args) == str:
                css = args
            elif type(args) == dict:
                css = args.get('css', '')
            else:
                return self.error('css不能为空')
            window.load_css(css)
            return self.success('加载css成功')
        except Exception as e:
            return self.error(f'加载css异常:{e}')

    def load_html(self, window, args):
        try:
            if type(args) == str:
                html = args
            elif type(args) == dict:
                html = args.get('html', '')
            else:
                return self.error('html不能为空')
            window.load_html(html)
            return self.success('加载html成功')
        except Exception as e:
            return self.error(f'加载html异常:{e}')

    def evaluate_js(self, window, args):
        try:
            if type(args) == str:
                js = args
            elif type(args) == dict:
                js = args.get('js', '')
            else:
                return self.error('js不能为空')
            window.evaluate_js(js)
            return self.success('执行js成功')
        except Exception as e:
            return self.error(f'执行js异常:{e}')

    def destroy(self, window, *args):
        try:
            window.destroy()
            return self.success('窗体销毁成功')
        except Exception as e:
            return self.error(f'窗口销毁异常:{e}')

    def hide(self, window, *args):
        try:
            window.hide()
            return self.success('窗体隐藏成功')
        except Exception as e:
            return self.error(f'窗口隐藏异常:{e}')

    def show(self, window, *args):
        try:
            window.show()
            return self.success('窗体显示成功')
        except Exception as e:
            return self.error(f'窗口显示异常:{e}')

    def minimize(self, window, *args):
        try:
            window.restore()
            window.minimize()
            return self.success('窗体最小化成功')
        except Exception as e:
            return self.error(f'窗口最小化异常:{e}')

    def screens(self, window, *args):
        try:
            import webview
            screens = webview.screens
            width, height = screens[0].width, screens[0].height
            return self.success('获取屏幕信息', {'width': width, 'height': height})
        except Exception as e:
            return self.error(f'获取屏幕信息异常:{e}')

    def toggle_fullscreen(self, window, *args):
        try:
            window.toggle_fullscreen()
            return self.success('切换全屏成功')
        except Exception as e:
            return self.error(f'切换全屏异常:{e}')

    def move(self, window, args=None):
        try:
            if type(args) == dict:
                x = args.get('x', 0)
                y = args.get('y', 0)
            else:
                return self.error('xy坐标不能为空')
            window.move(x, y)
            return self.success('窗口移动成功')
        except Exception as e:
            return self.error(f'窗口移动异常:{e}')

    def resize(self, window, args=None):
        try:
            if type(args) == dict:
                width = args.get('width', 0)
                height = args.get('height', 0)
            else:
                return self.error('宽高坐标不能为空')
            window.resize(width, height)
            return self.success('窗口大小设置成功')
        except Exception as e:
            return self.error(f'窗口大小设置异常:{e}')

    def open_file_dialog(self, window, args=None):
        try:
            import webview
            if type(args) != dict:
                return self.error('打开目录窗口参数异常')
            file_type = args.get('file_type', 'Image Files (*.bmp;*.jpg;*.gif)')
            file_types = (file_type, 'All files (*.*)')
            allow_multiple = args.get('allow_multiple', True)
            files = window.create_file_dialog(
                dialog_type=webview.OPEN_DIALOG,
                allow_multiple=allow_multiple,
                file_types=file_types
            )

            return self.success('打开目录窗口获取文件成功', {files: files})
        except Exception as e:
            return self.error(f'打开目录窗口异常:{e}')

    def save_file_dialog(self, window, args=None):
        try:
            import webview
            if type(args) != dict:
                return self.error('保存文件参数异常')
            directory = args.get('directory', '/')
            filename = args.get('filename', 'file')
            allow_multiple = args.get('allow_multiple', False)
            files = window.create_file_dialog(
                dialog_type=webview.SAVE_DIALOG,
                directory=directory,
                allow_multiple=allow_multiple,
                save_filename=filename
            )
            return self.success('保存文件成功', {files: files})
        except Exception as e:
            return self.error(f'保存文件异常:{e}')
