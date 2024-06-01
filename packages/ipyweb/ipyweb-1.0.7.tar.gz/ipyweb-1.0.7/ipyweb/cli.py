import click
from ipyweb.command import command


@click.group()
def main():
    pass


commands = command().load().getCommands()
if commands and type(commands) == dict and len(commands) > 0:
    for name, cmd in commands.items():
        main.add_command(cmd)

if __name__ == '__main__':
    main()
