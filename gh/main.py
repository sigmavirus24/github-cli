from gh.base import CustomOptionParser, load_command, commands
import sys


def main():
    prog = sys.argv[0]
    parser = CustomOptionParser()
    opts, args = parser.parse_args()

    if opts.help and not args:
        args = ['help']

    if not args:
        parser.error('You must provide a command. Use `{0} help`'.format(
            prog))

    repository = ()
    if '/' in args[0]:
        repository = args[0].split('/')
        args = args[1:]

    command = args[0].lower()
    load_command(command)
    if command in commands:
        commands[command].repository = repository
        commands[command].run(opts, args[1:])
