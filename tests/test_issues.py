import github3
from gh.util import tc
from gh.base import main_parser
from gh.commands.issue import IssueCommand
from gh.commands.issue.ls import IssueLsCommand
from base import BaseTest
from mock import patch


class TestIssueCommand(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestIssueCommand, self).__init__(methodName)
        self.issue = github3.issues.Issue(self.json('issue'))
        self.command = IssueCommand()
        self.command.repository = ('sigmavirus24', 'github3.py')
        self.opts, _ = self.command.parser.parse_args([])
        self.command.repo = github3.repos.Repository(self.json('issue'))

    def test_run(self):
        opts, args = main_parser.parse_args(['issue', '30', 'comments'])
        SUCCESS = self.command.SUCCESS
        FAILURE = self.command.FAILURE
        with patch.object(IssueCommand, 'get_repo'):
            with patch.object(self.command.repo, 'issue') as issue:
                issue.return_value = self.issue
                assert self.command.run(opts, args[1:]) == SUCCESS
                assert self.command.run(opts, ['foo']) == FAILURE


class TestIssueLsCommand(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestIssueLsCommand, self).__init__(methodName)
        self.issue = github3.issues.Issue(self.json('issue'))
        self.command = IssueLsCommand()
        self.command.repository = ('sigmavirus24', 'github3.py')
        self.opts, _ = self.command.parser.parse_args([])
        self.command.repo = github3.repos.Repository(self.json('issue'))

    def test_format_short_issue(self):
        out = self.command.format_short_issue(self.issue)
        assert tc['default'] in out
        assert tc['bold'] in out
        assert 'sigmavirus24' in out
        assert '30' in out

    def test_run(self):
        opts, args = main_parser.parse_args(['issue.ls', '-n', '5'])
        SUCCESS = self.command.SUCCESS
        with patch.object(IssueCommand, 'get_repo'):
            with patch.object(self.command.repo, 'issue') as issue:
                issue.return_value = self.issue
                assert self.command.run(opts, args[1:]) == SUCCESS
