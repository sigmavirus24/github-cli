from gh.base import main_parser, load_command, commands
from gh.util import get_repository_tuple
import sys


def main():
    opts, args = main_parser.parse_args()

    if opts.help and not args:
        args = ['help']

    if not args:
        main_parser.error('You must provide a command. '
                          '(Use `gh help` to see a list of commands)')

    repository = ()
    if '/' in args[0]:
        repository = args[0].split('/')
        args = args[1:]

    if opts.loc_aware and not repository:
        repository = get_repository_tuple()

    command = args[0].lower()
    load_command(command)
    status = 1

    if command in commands:
        commands[command].repository = repository
        status = commands[command].run(opts, args[1:])
        if status == commands[command].COMMAND_UNKNOWN:
            print('Unknown subcommand or option.')
            commands[command].help()

    sys.exit(status)
