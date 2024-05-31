import os
import click
import subprocess
from ipyweb.app import app
from ipyweb.ipyweb import ipyweb
from ipyweb.utils import utils


class ipywebRunner:

    @click.command(help='ipyweb run [appName]')
    @click.argument('name', nargs=1, default='', type=str)
    def run(name=os.environ.get('appName')):
        if name == '':
            click.echo(f'please input app name.')
            return
        click.echo(f'[{name}] ready ipyweb backend running...')
        app.setName(name)  # 动态设置应用名称
        ipyweb.boot(name)

    @click.command(help='ipyweb frontDev [appName] [background]')
    @click.argument('name', nargs=1, default='', type=str)
    @click.argument('background', nargs=1, default='', type=str)
    def frontDev(name=os.environ.get('appName'), background=''):
        if name == '':
            click.echo(f'please input app name.')
            return
        click.echo(f'[{name}] ready ipyweb fontend running...')
        app.setName(name)  # 动态设置应用名称
        ipyweb.bootBaser(True)

        directory = app.path(f'app/{name}/{app.frontendName}', True)
        os.chdir(directory)
        command = ['npm', 'run', 'dev']
        if background == 'd':
            command = ['start', '/b', 'npm', 'run', 'dev'] if utils.os() == 'win' else ['npm', 'run', 'dev', '&']
        subprocess.run(command, shell=True, check=True, text=True)
        # with subprocess.Popen(command, cwd=directory, shell=True) as process:
        #     process.wait()

    @click.command(help='ipyweb frontBuild [appName]')
    @click.argument('name', nargs=1, default='', type=str)
    def frontBuild(name=os.environ.get('appName')):
        if name == '':
            click.echo(f'please input app name.')
            return
        click.echo(f'[{name}] ready ipyweb fontend running...')
        app.setName(name)  # 动态设置应用名称
        ipyweb.bootBaser(True)

        directory = app.path(f'app/{name}/{app.frontendName}', True)
        os.chdir(directory)
        command = ['yarn','build']
        subprocess.run(command, shell=True, check=True, text=True)
