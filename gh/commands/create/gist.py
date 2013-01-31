import os
from gh.base import Command
from gh.util import read_stdin


class CreateGistCommand(Command):
    name = 'create.gist'
    usage = '%prog [options] create.gist [options] file1 file2'
    summary = 'Create a new gist'

    def __init__(self):
        super(CreateGistCommand, self).__init__()
        add = self.parser.add_option
        add('-p', '--private',
            dest='private',
            help='Make this gist private',
            default=False,
            action='store_true',
            )
        add('-d', '--description',
            dest='description',
            help='Description of the gist',
            type='str',
            default='',
            nargs=1,
            )
        self.parser.epilog('create.gist will accept stdin if you use `-` to'
                           'indicate that is your intention')

    def run(self, options, args):
        opts, args = self.parser.parse_args(args)

        if opts.help:
            self.help()

        status = self.COMMAND_UNKNOWN

        if not args:
            self.parser.print_help()
            return self.FAILURE

        status = self.FAILURE
        files = {}

        if '-' == args[0]:
            files['stdin'] = read_stdin()
        else:
            for f in args:
                base = os.path.basename(f)
                files[f] = {'content': open(f, 'rb').read()}

        # Create the gist
        g = self.gh.create_gist(opts.description, files, not opts.private)

        if g:
            print('{0.id} -- {0.html_url}'.format(g))
            status = self.SUCCESS

        return success
