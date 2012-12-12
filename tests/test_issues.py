import github3
import json
from gh.util import tc
from gh.base import main_parser
from gh.commands.issues import IssuesCommand
from base import BaseTest
from mock import patch


class TestIssuesCommand(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestIssuesCommand, self).__init__(methodName)
        self.issue = github3.issues.Issue(json.load(open('tests/json/issue')))
        self.command = IssuesCommand()
        self.command.repository = ('sigmavirus24', 'github3.py')
        self.opts, _ = self.command.parser.parse_args([])
        self.command.repo = github3.repos.Repository(
            json.load(open('tests/json/issue')))

    def test_format_short_issue(self):
        out = self.command.format_short_issue(self.issue)
        assert tc['default'] in out
        assert tc['bold'] in out
        assert 'sigmavirus24' in out
        assert '30' in out

    def test_format_long_issue(self):
        short = self.command.format_short_issue(self.issue)
        long = self.command.format_long_issue(self.issue)
        assert short in long

    def test_run(self):
        opts, args = main_parser.parse_args(['issues', '30', 'comments'])
        SUCCESS = self.command.SUCCESS
        COMMAND_UNKNOWN = self.command.COMMAND_UNKNOWN
        with patch.object(IssuesCommand, 'get_repo'):
            with patch.object(self.command.repo, 'issue') as issue:
                issue.return_value = self.issue
                assert self.command.run(opts, args[1:]) == SUCCESS
                assert self.command.run(opts, ['foo']) == COMMAND_UNKNOWN
