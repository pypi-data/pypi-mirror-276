import os, subprocess
import click
from ipyweb.app import app
from ipyweb.ipyweb import ipyweb
from ipyweb.builds.builder import builder


class ipywebBuilder:

    @click.command(help='ipyweb build [appName]')
    @click.argument('name', nargs=1, default='', type=str)
    def build(name=os.environ.get('appName')):

        app.setName(name)  # 动态设置应用名称
        ipyweb.bootBaser(True)
        command = ['python', 'cli.py', 'buildcli', name]
        subprocess.run(command, shell=True, check=True, text=True)

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
