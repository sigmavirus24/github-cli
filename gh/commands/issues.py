from gh.base import Command
from gh.util import tc, wrap


class IssuesCommand(Command):
    name = 'issues'
    usage = '%prog [user/repo] issues [OPTIONS] [sub-command(s)]'
    summary = 'Interact with the Issues API'
    fs = ('#{bold}{0.number}{default} {0.title:.36} - '
            '@{underline}{u.login}{default}')

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
        if not (self.repo or options.loc_aware):
            self.parser.error('issues requires a repository')

        opts, args = self.parser.parse_args(args)

        if not args and self.repo:
            iter = self.repo.iter_issues(opts.milestone, opts.state,
                    direction=opts.direction, mentioned=opts.mentioned,
                    number=opts.number)
            for i in iter:
                print(self.format_short_issue(i))
            return 0

        if args[0].startswith('#'):
            args[0] = args[1:]

        if args[0].isdigit():
            return self.single_issue(args[0], opts, args[1:])

    def format_comment(self, comment):
        fs = '@{uline}{u.login}{default} -- {date}\n{body}\n'
        body = '\n'.join(wrap(comment.body_text))
        date = comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return fs.format(u=comment.user, uline=tc['underline'],
                default=tc['default'], date=date, body=body)

    def format_long_issue(self, issue):
        text = "{0}\n--\n{1}"
        title = self.format_short_issue(issue)
        body = '\n'.join(wrap(issue.body_text))
        return text.format(title, body)

    def format_short_issue(self, issue):
        return self.fs.format(issue, u=issue.user, **tc)

    def single_issue(self, number, opts, args):
        status = 0
        issue = self.repo.issue(number)
        if not args:
            print(self.format_long_issue(issue))
        elif 'comments' in args:
            for c in issue.iter_comments(opts.number):
                print(self.format_comment(c))
        elif 'close' in args:
            issue.close()
        elif 'reopen' in args:
            issue.reopen()
        else:
            status = 1
        return status


# Ensures this ends up in gh.base.commands
IssuesCommand()
