from gh.base import Command
from gh.util import tc, wrap


class IssuesCommand(Command):
    name = 'issues'
    usage = ('%prog [options] [user/repo] issues [options] [number]'
            ' [sub-command]')
    summary = 'Interact with the Issues API'
    fs = ('#{bold}{0.number}{default} {0.title:.36} - @{u.login}')
    subcommands = {
            '[#]1': 'Print the full issue',
            '[#]1 comments': 'Print all the comments on this issue',
            '[#]1 close': 'Close this issue',
            '[#]1 reopen': 'Reopen this issue',
            '[#]1 assign <assignee>': 'Assign this issue to @<assignee>',
            }

    def __init__(self):
        super(IssuesCommand, self).__init__()
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

        if not args:
            iter = self.repo.iter_issues(opts.milestone, opts.state,
                    direction=opts.direction, mentioned=opts.mentioned,
                    number=opts.number)
            for i in iter:
                print(self.format_short_issue(i))
            return 0

        if args[0].startswith('#'):
            args[0] = args[1:]

        if not args[0].isdigit():
            return -1

        status = 0
        number = args.pop(0)

        subcommand = None
        if args:
            subcommand = args[0].lower()

        if not subcommand:
            issue = self.repo.issue(number)
            print(self.format_long_issue(issue))
        elif 'comments' == subcommand:
            status = self.print_comments(number, opts)
        elif 'close' == subcommand:
            status = self.close_issue(number)
        elif 'reopen' == subcommand:
            status = self.reopn_issue(number)
        elif args and ('assign' == subcommand):
            self.assign(number, args[0])
        else:
            print('Unrecognized subcommand "{0}"'.format(subcommand))
            self.help()
            status = -1

        return status

    def format_comment(self, comment):
        fs = '@{uline}{u.login}{default} -- {date}\n{body}\n'
        body = '\n'.join(wrap(comment.body_text))
        date = comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return fs.format(u=comment.user, uline=tc['underline'],
                default=tc['default'], date=date, body=body)

    def format_long_issue(self, issue):
        format_str = '{header}\n{sep}\n{body}\n'
        sep = '-' * 78
        title = self.format_short_issue(issue)
        body = '\n'.join(wrap(issue.body_text))
        return format_str.format(header=title, sep=sep, body=body)

    def format_short_issue(self, issue):
        extra = []
        if issue.milestone:
            extra.append(issue.milestone.title)
        if issue.assignee:
            extra.append(issue.assignee.login)
        if extra:
            extra = '(' + ' -- '.join(extra) + ')'
        else:
            extra = ''
        return self.fs.format(issue, u=issue.user, bold=tc['bold'],
                default=tc['default']) + extra

    def print_comments(self, number, opts):
        issue = self.repo.issue(number)
        if not issue:
            return -1
        for c in issue.iter_comments(opts.number):
            print(self.format_comment(c))
        return 0

    def _get_authenticated_issue(self, number):
        self.login()
        user, repo = self.repository
        return self.gh.issue(user, repo, number)

    def close_issue(self, number):
        issue = self._get_authenticated_issue(number)
        if not issue:
            return -1
        issue.close()
        return 0

    def reopen_issue(self, number):
        issue = self._get_authenticated_issue(number)
        if not issue:
            return -1
        issue.reopen()
        return 0

    def assign(self, number, assignee):
        issue = self._get_authenticated_issue(number)
        if not issue:
            return -1
        issue.assign(assignee)
        return 0

# Ensures this ends up in gh.base.commands
IssuesCommand()
