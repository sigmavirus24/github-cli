from gh.base import Command


class CreatePullCommand(Command):
    name = 'create.pull'
    usage = '%prog [options] create.pull [options] base head'
    summary = 'Create a new pull request'
    subcommands = {}

    def __init__(self):
        super(CreatePullCommand, self).__init__()
        add = self.parser.add_option
        add('-i', '--from-issue',
            dest='issue',
            help='Create the pull from issue provided',
            type='int',
            default=-1,
            nargs=1,
            )
        add('-t', '--title',
            dest='title',
            help='Title for a new pull request',
            type='str',
            default='',
            nargs=1,
            )

    def run(self, options, args):
        self.get_repo(options)
        opts, args = self.parser.parse_args(args)

        if opts.help:
            self.parser.print_help()
            return self.SUCCESS

        if opts.issue < 1 and not (opts.title and len(args) >= 2):
            self.parser.error('You must either specify an issue number or a'
                              ' title as well as the base and head for the'
                              ' pull.')
            self.parser.print_help()
            return self.FAILURE

        self.login()

        status = self.SUCCESS
        if opts.issue > 1:
            pr = self.repo.create_pull_from_issue(
                opts.issue, args[0], args[1])
        else:
            pr = self.repo.create_pull(opts.title, args[0], args[1])

        if not pr:
            status = self.FAILURE
        else:
            print('#{0.number} {0.html_url}'.format(pr))

        return status


CreatePullCommand()
