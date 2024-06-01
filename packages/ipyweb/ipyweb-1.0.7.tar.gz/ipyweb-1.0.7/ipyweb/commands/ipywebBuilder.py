import os, subprocess,click
from ipyweb.app import app
from ipyweb.ipyweb import ipyweb
from ipyweb.builds.builder import builder
from ipyweb.utils import utils


class ipywebBuilder:

    @click.command(help='ipyweb build [appName]')
    @click.argument('name', nargs=1, default='', type=str)
    def build(name=os.environ.get('appName')):

        app.setName(name)  # 动态设置应用名称
        ipyweb.bootBaser(True)
        command = ['python', 'cli.py', 'buildcli', name]
        subprocess.run(command, shell=utils.isWin(), check=True, text=True)

    @click.command(help='python cli.py  buildcli [appName]')
    @click.argument('name', nargs=1, default='', type=str)
    def buildcli(name=os.environ.get('appName')):
        try:
            import PyInstaller
        except ImportError:
            click.echo(f'please install PyInstaller.')
            return

        if name == '':
            click.echo(f'please input app name.')
            return
        cmds = builder.run(name).getCmds()
        try:
            from PyInstaller import __main__ as pyiMain
            pyiMain.run(cmds)
            click.echo(f'build finished.')
            builder.clear()
        except Exception as e:
            click.echo(f"build exception:{e}")

    @click.command(help='ipyweb fbuild [appName]')
    @click.argument('name', nargs=1, default='', type=str)
    def fbuild(name=os.environ.get('appName')):
        if name == '':
            click.echo(f'please input app name.')
            return
        click.echo(f'[{name}] ready ipyweb fontend running...')
        app.setName(name)  # 动态设置应用名称
        ipyweb.bootBaser(True)

        directory = app.path(f'app/{name}/{app.frontendName}', True)
        os.chdir(directory)
        command = ['yarn', 'build']
        subprocess.run(command, shell=utils.isWin(), check=True, text=True)
