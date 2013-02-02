from gh.base import Command
from gh.util import tc, wrap, trim_numbers, get_issue_number


class IssueCommentsCommand(Command):
    name = 'issue.comments'
    usage = '%prog [options] issue.comments [#]number'
    summary = 'Print the comments for an issue'
    subcommands = {}

    def __init__(self):
        super(IssueCommentsCommand, self).__init__()
        add = self.parser.add_option
        add('-n', '--number',
            dest='number',
            help='Number of comments to list',
            default=-1,
            type='int',
            )

    def run(self, options, args):
        self.get_repo(options)

        opts, args = self.parser.parse_args(args)

        if opts.help:
            self.help()

        number = get_issue_number(
            args, self.parser, 'issue.comments requires a valid issue number'
        )
        if number is None:
            return self.FAILURE

        return self.print_comments(number, opts)

    def format_comment(self, comment):
        fs = '@{uline}{u.login}{default} -- {date}\n{body}\n'
        body = wrap(comment.body_text)
        date = comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return fs.format(u=comment.user, uline=tc['underline'],
                         default=tc['default'], date=date, body=body)

    def print_comments(self, number, opts):
        issue = self.repo.issue(number)

        if not issue:
            return self.FAILURE

        for c in issue.iter_comments(opts.number):
            print(self.format_comment(c))

        return self.SUCCESS


IssueCommentsCommand()
