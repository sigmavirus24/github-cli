from gh.base import Command
from gh.util import tc
from github3.users import User


class ReposCommand(Command):
    name = 'repos'
    usage = ('%prog [options] repos [options] [login] [sub-command]')
    summary = ('Interact with the Repositories API')
    fs = ("{d[bold]}{0.name}{d[default]}\n  {1:.72}")
    fs2 = ("{d[bold]}{0.name}{d[default]}")
    subcommands = {}

    def __init__(self):
        super(ReposCommand, self).__init__()
        self.parser.add_option('-t', '--type',
                               dest='type',
                               help='Which repositories to list',
                               choices=('all', 'owner', 'public', 'private',
                                        'member'),
                               default='all',
                               nargs=1,
                               )
        self.parser.add_option('-s', '--sort',
                               dest='sort',
                               help='How to sort the listed repositories',
                               choices=('created', 'updated', 'pushed',
                                        'name'),
                               nargs=1,
                               )
        self.parser.add_option('-d', '--direction',
                               dest='direction',
                               help='Which direction to list them in',
                               choices=('asc', 'desc'),
                               nargs=1,
                               )
        self.parser.add_option('-n', '--number',
                               dest='number',
                               help='Number of repositories to list',
                               type='int',
                               default=-1,
                               nargs=1,
                               )

    def run(self, options, args):
        opts, args = self.parser.parse_args(args)

        if opts.help:
            self.help()

        if opts.sort == 'name':
            opts.sort = 'full_name'

        if args:
            user = args.pop(0)
        else:
            user = self.get_user()

        kwargs = {
            'type': opts.type,
            'sort': opts.sort,
            'direction': opts.direction,
            'number': opts.number
        }

        if isinstance(user, User):
            repos = self.gh.iter_repos(**kwargs)
        else:
            repos = self.gh.iter_repos(self.user, **kwargs)

        for repo in repos:
            fs = self.fs if repo.description else self.fs2
            print(fs.format(repo, repo.description.encode('utf-8'), d=tc))

        return self.SUCCESS


ReposCommand()
