from gh.base import Command, CustomOptionParser
from gh.util import tc


class GistsCommand(Command):
    name = 'gists'
    usage = '%prog [options] gists [options] [sub-commands]'
    summary = 'Interact with the Gists API'
    subcommands = {
        'create': 'Create a new gist'
    }
    gist_fs = '{0[bold]}{id}{0[default]} -- {desc}'

    def __init__(self):
        super(GistsCommand, self).__init__()
        add = self.parser.add_option
        add('-u', '--username',
            dest='username',
            help="Lists this user's gists",
            type='str',
            default='',
            nargs=1,
            )
        add('-n', '--number',
            dest='number',
            help='Number of gists to list',
            type=int,
            default=-1,
            nargs=1,
            )

    def run(self, options, args):
        opts, args = self.parser.parse_args(args)

        if opts.help:
            self.help()

        status = self.COMMAND_UNKNOWN

        if not args:
            status = self.gists(opts.username, opts.number)
        elif args[0] == 'create':
            status = self.create(args[1:])

        return status

    def gists(self, username, number):
        if not username:
            self.login()

        for g in self.gh.iter_gists(username, number):
            self.print_gist(g)

    def create(self, args):
        self.login()

        parser = CustomOptionParser('%prog [options] gists create [options] '
                                    'file_0 file_1 ...')
        add = parser.add_option
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

        opts, args = parser.parse_args(args)

        if not args:
            parser.print_help()
            return self.FAILURE

        files = {}
        for f in args:
            files[f] = {'content': open(f).read()}

        g = self.gh.create_gist(opts.description, files, not opts.private)
        self.print_gist(g)
        return self.SUCCESS

    def print_gist(self, gist):
        print(self.gist_fs.format(tc, id=gist.id, desc=gist.description))
        self.print_files(gist)

    def print_files(self, gist):
        for f in gist.iter_files():
            print('  {0}: {1} {2}'.format(f.filename, f.language, f.size))


GistsCommand()
