from gh.base import Command
from gh.util import tc


class PullsCommand(Command):
    name = 'pulls'
    usage = ('%prog [options] [user/repo] pulls [options] [number]'
            ' [sub-command]')
    summary = 'Interact with the Pull Requests API'
    fs = ('#{bold}{0.number}{default} {0.title:.36} - @{u.login}')
    subcommands = {}

    def __init__(self):
        super(PullsCommand, self).__init__()
        self.parser.add_option('-s', '--state',
                dest='state',
                help='State of the pull request.',
                choices=('open', 'closed'),
                default='open',
                nargs=1,
                )
        self.parser.add_option('-n', '--number',
                dest='number',
                help='Number of pulls to list',
                type='int',
                nargs=1,
                default=-1,
                )

    def run(self, options, args):
        self.get_repo(options)

        opts, args = self.parser.parse_args(args)

        if not args:
            for p in self.repo.iter_pulls(opts.state, opts.number):
                print(self.fs.format(p, u=p.user, bold=tc['bold'],
                    default=tc['default']))
                for f in p.iter_files():
                    print('  {0}: +{1}/-{2}'.format(f.filename, f.additions,
                        f.deletions))


PullsCommand()
