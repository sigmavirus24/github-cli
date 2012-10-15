from github3 import issue
from gh.util import tc
from gh.base import main_parser
from gh.commands.issues import IssuesCommand
from base import BaseTest


class TestIssuesCommand(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestIssuesCommand, self).__init__(methodName)
        self.issue = issue('sigmavirus24', 'github3.py', 30)
        self.command = IssuesCommand()
        self.command.repository = ('sigmavirus24', 'github3.py')
        self.opts, _ = self.command.parser.parse_args([])
        self.command.get_repo(self.opts)

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
        assert self.command.run(opts, args[1:]) == self.command.SUCCESS
        assert self.command.run(opts, ['foo']) == self.command.COMMAND_UNKNOWN
