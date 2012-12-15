from gh.base import Command


class UnfollowCommand(Command):
    name = 'unfollow'
    usage = '%prog [options] unfollow login'
    summary = 'Un-follow a user'
    subcommands = {}

    def __init__(self):
        super(UnfollowCommand, self).__init__()

    def run(self, options, args):
        opts, args = self.parser.parse_args(args)

        status = self.SUCCESS
        self.login()

        if opts.help:
            self.help()

        if not args:
            self.parser.error('A login is required to unfollow someone')
            status = self.FAILURE

        else:
            if not self.gh.unfollow(args[0]):
                status = self.FAILURE

        return status


UnfollowCommand()
