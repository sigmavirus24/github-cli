from gh.base import Command
from gh.util import tc
from gh.compat import input
from github3.users import User


class ReposCommand(Command):
    name = 'repos'
    usage = ('%prog [options] repos [options] [login] [sub-command]')
    summary = ('Interact with the Repositories API')
    fs = ("{d[bold]}{0.name}{d[default]}\n  {1:.72}")
    fs2 = ("{d[bold]}{0.name}{d[default]}")
    subcommands = {
        'create [name]': 'Create a new repository with given name',
    }
    commands = set(['create'])

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
        self.parser.add_option('-o', '--organization',
                               dest='organization',
                               help=('Organization to create this repository '
                                     'under'),
                               type='str',
                               default='',
                               nargs=1,
                               )

    def run(self, options, args):
        opts, args = self.parser.parse_args(args)

        if opts.help:
            self.help()

        if opts.sort == 'name':
            opts.sort = 'full_name'

        if not args or args[0] not in self.commands:
            if args:
                self.user = args.pop(0)
            else:
                self.get_user()
            return self.print_repos(opts)

        cmd = args.pop(0)
        if cmd not in self.commands:
            return self.COMMAND_UNKNOWN

        if cmd == 'create':
            self.create(opts, args)

    def print_repos(self, opts):
        kwargs = {
            'type': opts.type,
            'sort': opts.sort,
            'direction': opts.direction,
            'number': opts.number
        }

        if isinstance(self.user, User):
            repos = self.gh.iter_repos(**kwargs)
        else:
            repos = self.gh.iter_repos(self.user, **kwargs)

        for repo in repos:
            fs = self.fs if repo.description else self.fs2
            print(fs.format(repo, repo.description.encode('utf-8'), d=tc))

        return self.SUCCESS

    def create(self, opts, args):
        status = self.SUCCESS
        org = None
        repo = None

        try:
            name = args.pop(0)
        except IndexError:
            self.parser.error("You must provide a name for your new "
                              "repository")
            return self.FAILURE

        self.login()

        if opts.organization:
            org = self.gh.organization(opts.organization)

        conf = {}
        conf['description'] = input('Description: ')
        conf['homepage'] = input('Website: ')
        conf['private'] = bool(input('Private [False]: ') or False)

        if org:
            teams = [t for t in org.iter_teams()]
            print('(Optional) Select team to add this to:')
            for i, t in enumerate(teams):
                print('\t[{0}] {1}'.format(i, t.name))

            i = int(input(''))
            conf['team_id'] = teams[i].id

            repo = org.create_repo(name, **conf)
        else:
            repo = self.gh.create_repo(name, **conf)

        if not repo:
            status = self.FAILURE

        return status


ReposCommand()
