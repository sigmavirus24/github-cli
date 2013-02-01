from pkgutil import walk_packages
from gh.base import Command, load_command, commands, main_parser
from gh import commands as cmds
from gh.commands import create
import os


class HelpCommand(Command):
    name = 'help'
    usage = '%prog help'
    summary = 'Display the help information'

    def __init__(self):
        super(HelpCommand, self).__init__()
        self.parser = main_parser

    def run(self, options, args):
        def load_subcommand(command, top_level_path):
            path = [os.path.join(top_level_path, command)]
            for _, cmd, __ in walk_packages(path=path):
                subcmd = '{0}.{1}'.format(command, cmd)
                load_command(subcmd)
                self.subcommands[subcmd] = commands[subcmd].summary

        if args:
            cmd = args[0].lower()
            load_command(cmd)
            if cmd not in commands:
                self.parser.error('No command named: {0}'.format(cmd))
            commands[cmd].help()
            return 0

        # Load all available commands
        for imp, command, ispkg in walk_packages(path=cmds.__path__):
            if ispkg:
                load_subcommand(command, cmds.__path__[0])
            else:
                load_command(command)
                self.subcommands[command] = commands[command].summary

        self.help()

        return 0

HelpCommand()
