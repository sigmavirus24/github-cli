from gh.base import Command
from gh.util import tc, wrap
from gh.compat import fix_encoding


class GistsCommand(Command):
    name = 'gists'
    usage = '%prog [options] gists [options] [gistid]'
    summary = 'Interact with the Gists API'
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

        if not opts.username:
            self.login()

        if args:
            self.print_gist(self.gh.gist(args[0]))
        else:
            for g in self.gh.iter_gists(opts.username, opts.number):
                self.short_gist(g)

        return self.SUCCESS

    def print_gist(self, gist):
        print('{0.html_url}: {0.description}'.format(gist))
        for f in gist.iter_files():
            f.content = fix_encoding(f.content)
            print(f.content)

    def short_gist(self, gist):
        print(self.gist_fs.format(tc, id=gist.id, desc=gist.description))
        self.print_files(gist)
        print('  {0}'.format(gist.html_url))

    def print_files(self, gist):
        for f in gist.iter_files():
            print('  {0}: {1} {2}'.format(f.filename, f.language, f.size))


GistsCommand()
