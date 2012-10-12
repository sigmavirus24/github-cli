from pkgutil import walk_packages
from gh.base import Command, load_command, commands, main_parser
from gh import commands as cmds


class HelpCommand(Command):
    name = 'help'
    usage = '%prog help'
    summary = 'Display the help information'

    def __init__(self):
        super(HelpCommand, self).__init__()
        self.parser = main_parser

    def run(self, options, args):
        def cmd_cmp(x, y):
            if x.name == y.name:
                return 0
            elif x.name > y.name:
                return 1
            return -1

        # Load all available commands
        for _, command, __ in walk_packages(path=cmds.__path__):
            load_command(command)
            self.subcommands[command] = commands[command].summary

        if args:
            cmd = args[0].lower()
            if cmd not in commands:
                self.parser.error('No command named: {0}'.format(cmd))
            commands[cmd].help()
            return 0

        self.help()

        return 0

HelpCommand()
