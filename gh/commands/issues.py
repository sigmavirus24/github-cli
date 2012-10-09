from gh.base import Command
from gh.util import get_repository_tuple
from github3 import repository


class IssuesCommand(Command):
    name = 'issues'

    def run(self, options, args):
        repo = None
        if self.repository:
            repo = repository(*self.repository)

        if not self.repository and options.loc_aware:
            repo = repository(*get_repository_tuple())

        if not args and repo:
            for i in repo.iter_issues():
                print self.format_issue(i)

    def format_issue(self, issue):
        fs = '[#{0.number}] {0.title:.36} - @{0.user.login}'
        return fs.format(issue)


# Ensures this ends up in gh.base.commands
IssuesCommand()
