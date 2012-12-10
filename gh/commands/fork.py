from gh.base import Command


class ForkCommand(Command):
    name = 'fork'
    usage = '%prog [options] fork [options] login/repo'
    summary = 'Fork a repository'
    subcommands = {}

    def __init__(self):
        super(ForkCommand, self).__init__()
        self.parser.add_option('-o', '--organization',
                               dest='organization',
                               help='Fork to an organization instead of user',
                               type='str',
                               default='',
                               nargs=1,
                               )

    def run(self, options, args):
        opts, args = self.parser.parse_args(args)
        self.login()

        if opts.help:
            self.help()

        if not args or '/' not in args[0]:
            self.parser.error('You must provide a repository name')
            return self.FAILURE

        self.repository = args[0].split('/')
        self.get_repo(options)

        fork = self.repo.create_fork(opts.organization)
        if fork.owner.login == self.repo.owner.login:
            self.parser.error('An error occurred and the repository was not '
                              'forked')
            return self.FAILURE

        print('git clone {0}'.format(fork.ssh_url))
        return self.SUCCESS


ForkCommand()
