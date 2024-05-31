import os
import click
from PyInstaller import __main__ as pyiMain
from ipyweb.builds.builder import builder


class ipywebBuilder:

    @click.command(help='run: py ipw.py build [appName]')
    @click.argument('name', nargs=1, default='', type=str)
    def build(name=os.environ.get('appName')):
        if name == '':
            click.echo(f'please input app name.')
            return
        cmds = builder.run(name).getCmds()
        try:
            pyiMain.run(cmds)
            click.echo(f'build finished.')
            builder.clear()
        except Exception as e:
            click.echo(f"build exception:{e}")
