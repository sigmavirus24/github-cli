from gh.base import main_parser, load_command, commands
import sys


def main():
    prog = sys.argv[0]
    opts, args = main_parser.parse_args()

    if opts.help and not args:
        args = ['help']

    if not args:
        main_parser.error('You must provide a command. Use `{0} help`'.format(
            prog))

    repository = ()
    if '/' in args[0]:
        repository = args[0].split('/')
        args = args[1:]

    command = args[0].lower()
    load_command(command)
    if command in commands:
        commands[command].repository = repository
        if command != 'help':
            commands[command].login()
        commands[command].run(opts, args[1:])
