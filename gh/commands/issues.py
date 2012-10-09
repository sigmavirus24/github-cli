from gh.base import Command
from gh.util import get_repository_tuple, tc
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
        fs = ('#{bold}{0.number}{default} {0.title:.36} - '
            '@{underline}{u.login}{default}')
        return fs.format(issue, u=issue.user, **tc)


# Ensures this ends up in gh.base.commands
IssuesCommand()
