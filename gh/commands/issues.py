from gh.basecommand import Command
from gh.util import get_repository_tuple
from github3 import repository


class IssuesCommand(Command):
    name = 'issues'

    def run(self, args):
        if not args:
            repo = repository(*get_repository_tuple())
            for i in repo.iter_issues():
                print self.format_issue(i)

    def format_issue(self, issue):
        fs = '[#{0.number}] {0.title:.18} - @{0.user.login}'
        return fs.format(issue)
