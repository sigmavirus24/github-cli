from gh.base import Command


class FollowCommand(Command):
    name = 'follow'
    usage = '%prog [options] follow login'
    summary = 'Follow a user'
    subcommands = {}

    def __init__(self):
        super(FollowCommand, self).__init__()

    def run(self, options, args):
        opts, args = self.parser.parse_args(args)
        status = self.SUCCESS
        self.login()

        if opts.help:
            self.help()

        if not args:
            for u in self.gh.iter_following():
                print(u.login)

        else:
            if not self.gh.follow(args[0]):
                status = self.FAILURE

        return status


FollowCommand()
