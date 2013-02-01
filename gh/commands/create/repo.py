from gh.base import Command
from gh.compat import input


class CreateRepoCommand(Command):
    name = 'create.repo'
    usage = '%prog [options] create.repo [options] name'
    summary = 'Create a new repository'
    subcommands = {}

    def __init__(self):
        super(CreateRepoCommand, self).__init__()
        add = self.parser.add_option
        add('-o', '--organization',
            dest='organization',
            help='Organization to create this repository under',
            type='str',
            default='',
            nargs=1,
            )

    def run(self, options, args):
        opts, args = self.parser.parse_args(args)

        if not args:
            self.parser.error('You must provide a name for your repository')
            return self.FAILURE

        name = args.pop(0)

        self.login()

        org = None
        if opts.organization:
            org = self.gh.organization(opts.organization)

        conf = {}
        conf['description'] = input('Description: ')
        conf['homepage'] = input('Website: ')
        conf['private'] = bool(input('Private [False]: ') or False)

        repo = None
        status = self.SUCCESS
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

        print("{0} {0.html_url}".format(repo))

        return status


CreateRepoCommand()
