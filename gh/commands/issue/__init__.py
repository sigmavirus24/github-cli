from gh.base import Command
from gh.util import trim_numbers, wrap, sep, tc, get_issue_number


class IssueCommand(Command):
    name = 'issue'
    usage = '%prog [options] issue [#]number'
    summary = 'View the issue specified'
    subcommands = {}

    def run(self, options, args):
        self.get_repo(options)
        opts, args = self.parser.parse_args(args)

        if opts.help:
            self.help()

        number = get_issue_number(
            args, self.parser, 'An issue number is required.'
        )

        if number is None:
            return self.FAILURE

        issue = self.repo.issue(number)

        format_str = '{header}\n{sep}\n{body}\n'
        title = ('#{0.number}: {1[bold]}{0.title}{1[default]} - '
                 '@{0.user}'.format(issue, tc))
        body = wrap(issue.body_text or '')
        print(format_str.format(header=title, sep=sep, body=body))
        return self.SUCCESS


IssueCommand()
