from pkgutil import walk_packages
from gh.base import Command, load_command, commands, main_parser
from gh import commands as cmds


class HelpCommand(Command):
    name = 'help'
    usage = '%prog'
    summary = 'Display the help information'

    def __init__(self):
        super(HelpCommand, self).__init__()

    def run(self, options, args):
        for _, command, __ in walk_packages(path=cmds.__path__):
            load_command(command)

        if args:
            cmd = args[0].lower()
            if cmd not in commands:
                self.parser.error('No command named: {0}'.format(cmd))
            commands[cmd].parser.print_help()
            return 0

        def cmd_cmp(x, y):
            if x.name == y.name:
                return 0
            elif x.name > y.name:
                return 1
            return -1

        main_parser.print_help()
        print('\nSubcommands:')
        for command in sorted(commands.values(), cmd_cmp):
            print('  {0.name}: {0.summary}'.format(command))

        return 0

HelpCommand()
