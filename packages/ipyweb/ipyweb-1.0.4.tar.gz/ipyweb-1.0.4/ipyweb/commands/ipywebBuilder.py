import os
import click

from ipyweb.builds.builder import builder


class ipywebBuilder:

    @click.command(help='ipyweb build [appName]')
    @click.argument('name', nargs=1, default='', type=str)
    def build(name=os.environ.get('appName')):
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
