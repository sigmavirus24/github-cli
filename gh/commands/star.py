from gh.base import Command


class StarCommand(Command):
    name = 'star'
    usage = '%prog [options] star [login/]repo'
    summary = 'Star a repository'
    subcommands = {}

    def __init__(self):
        super(StarCommand, self).__init__()
        self.parser.epilog = ("If you don't specify a login, we will assume"
                              " that you own the repository you wish to "
                              "star.")

    def run(self, options, args):
        if not args:
            self.parser.error('You must provide a repository')
            return self.FAILURE

        self.login()

        repo = args.pop(0)
        if '/' not in repo:
            repo = (self.user, repo)
        else:
            repo = repo.split('/', 1)

        if self.gh.star(*repo):
            print("Starred {0}/{1}".format(*repo))
            return self.SUCCESS

        self.parser.error("Could not star {0}/{1}".format(*repo))
        return self.FAILURE


StarCommand()
