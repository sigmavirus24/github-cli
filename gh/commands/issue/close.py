from gh.base import Command
from gh.util import get_issue_number


class IssueCloseCommand(Command):
    name = 'issue.close'
    usage = '%prog [options] issue.close [#]number'
    summary = 'Close an issue'
    subcommands = {}

    def run(self, options, args):
        self.get_repo(options)

        opts, args = self.parser.parse_args(args)

        if opts.help:
            self.help()

        number = get_issue_number(
            args, self.parser, 'issue.close requires a valid number'
        )

        if number is None:
            return self.FAILURE

        return self.close_issue(number)

    def close_issue(self, number):
        self.login()
        user, repo = self.repository
        issue = self.gh.issue(user, repo, number)
        if not issue:
            return self.FAILURE
        if issue.close():
            return self.SUCCESS
        else:
            return self.FAILURE

IssueCloseCommand()
