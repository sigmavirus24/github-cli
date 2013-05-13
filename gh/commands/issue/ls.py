from gh.base import Command
from gh.util import tc
from gh.compat import fix_encoding


class IssueLsCommand(Command):
    name = 'issue.ls'
    usage = '%prog [options] issues.ls [options]'
    summary = 'Interact with the Issues API'
    fs = '#{0.number:<%d} {bold}{0.title}{default} - @{0.user}'
    subcommands = {}

    def __init__(self):
        super(IssueLsCommand, self).__init__()
        self.parser.add_option('-d', '--direction',
                               dest='direction',
                               help='How to list issues on a repository',
                               choices=('asc', 'desc'),
                               nargs=1,
                               )
        self.parser.add_option('-s', '--state',
                               dest='state',
                               help='State of issues to list',
                               choices=('open', 'closed'),
                               default='open',
                               nargs=1
                               )
        self.parser.add_option('-m', '--milestone',
                               dest='milestone',
                               help='Milestone to list issues on',
                               type='int',
                               nargs=1,
                               )
        self.parser.add_option('-M', '--mentioned',
                               dest='mentioned',
                               help='List issues mentioning specified user',
                               type='str',
                               nargs=1,
                               )
        self.parser.add_option('-n', '--number',
                               dest='number',
                               help='Number of issues to list at most',
                               type='int',
                               nargs=1,
                               default=-1,
                               )

    def run(self, options, args):
        self.get_repo(options)

        opts, args = self.parser.parse_args(args)

        if opts.help:
            self.help()

        return self.print_issues(opts)

    # Formatting and printing
    def format_short_issue(self, issue):
        extra = []

        if issue.milestone:
            extra.append(issue.milestone.title)

        if issue.assignee:
            extra.append(issue.assignee.login)

        if extra:
            extra = ' (' + ' -- '.join(extra) + ')'
        else:
            extra = ''

        issue.title = fix_encoding(issue.title)

        return (self.fs.format(issue, bold=tc['bold'], default=tc['default'])
                + extra)

    def print_issues(self, opts):
        status = self.SUCCESS
        issues = self.repo.iter_issues(
            opts.milestone, opts.state, direction=opts.direction,
            mentioned=opts.mentioned, number=opts.number
        )

        num_width_set = False
        for i in issues:
            if not num_width_set:
                n = i.number
                width = 1
                while n > 1:
                    n /= 10
                    width += 1
                self.fs %= width
                num_width_set = True
            print(self.format_short_issue(i))

        return status

    # Administration/interaction
    def _get_authenticated_issue(self, number):
        self.login()
        user, repo = self.repository
        return self.gh.issue(user, repo, number)

    def close_issue(self, number):
        issue = self._get_authenticated_issue(number)

        if not issue:
            return self.FAILURE
        issue.close()

        return self.SUCCESS

    def reopen_issue(self, number):
        issue = self._get_authenticated_issue(number)

        if not issue:
            return self.FAILURE
        issue.reopen()

        return self.SUCCESS

    def assign(self, number, assignee):
        issue = self._get_authenticated_issue(number)

        if not issue:
            return self.FAILURE
        issue.assign(assignee)

        return self.SUCCESS

# Ensures this ends up in gh.base.commands
IssueLsCommand()
