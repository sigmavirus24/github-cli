from gh.base import Command
from gh.util import get_issue_number


class IssueReopenCommand(Command):
    name = 'issue.reopen'
    usage = '%prog [options] issue.reopen [#]number'
    summary = 'Reopen an issue'
    subcommands = {}

    def run(self, options, args):
        self.get_repo(options)

        opts, args = self.parser.parse_args(args)

        if opts.help:
            self.help()

        number = get_issue_number(
            args, self.parser, 'issue.reopen requires a valid number'
        )

        if number is None:
            return self.FAILURE

        return self.reopen_issue(number)

    def reopen_issue(self, number):
        self.login()
        user, repo = self.repository
        issue = self.gh.issue(user, repo, number)
        if not issue:
            print("Reopening issue failed.")
            return self.FAILURE
        if issue.reopen():
            print("Issue reopened successfully.")
            return self.SUCCESS
        else:
            print("Reopening issue failed.")
            return self.FAILURE

IssueReopenCommand()
