from gh.base import Command
from gh.util import get_issue_number
from gh.util import mktmpfile, rmtmpfile


class IssueAssignCommand(Command):
    name = 'issue.assign'
    usage = '%prog [options] issue.assign [#]number assignee'
    summary = 'Assign an issue'
    subcommands = {}

    def run(self, options, args):
        self.get_repo(options)

        opts, args = self.parser.parse_args(args)

        if len(args) != 2:
            print('issue.assign requires 2 arguments.')
            self.help()
            return self.FAILURE

        if opts.help:
            self.help()

        number = get_issue_number(
            args, self.parser, 'issue.reopen requires a valid number'
        )

        if number is None:
            return self.FAILURE

        return self.assign_issue(number, args[1])

    def assign_issue(self, number, assignee):
        self.login()
        user, repo = self.repository
        issue = self.gh.issue(user, repo, number)
        if not issue:
            print("Couldn't get an issule {0}#{1}".format(repo, number))
            return self.FAILURE
        if issue.assign(assignee):
            print("Issue assigned successfully.")
            return self.SUCCESS
        else:
            print("Assigning issue failed.")
            return self.FAILURE

IssueAssignCommand()
