from unittest import TestCase
from github3 import issue
from gh.util import tc
from gh.commands.issues import IssuesCommand
import sys
import os


class TestIssuesCommand(TestCase):
    def __init__(self, methodName='runTest'):
        super(TestIssuesCommand, self).__init__(methodName)
        self.issue = issue('sigmavirus24', 'github3.py', 30)
        self.command = IssuesCommand()
        self.command.repository = ('sigmavirus24', 'github3.py')
        self.opts, _ = self.command.parser.parse_args([])
        self.command.get_repo(self.opts)

    def setUp(self):
        self.stdout = sys.stdout
        sys.stdout = open(os.devnull, 'r+')

    def tearDown(self):
        sys.stdout.close()
        sys.stdout = self.stdout

    def test_format_short_issue(self):
        out = self.command.format_short_issue(self.issue)
        assert tc['default'] in out
        assert tc['bold'] in out
        assert tc['underline'] in out
        assert 'sigmavirus24' in out
        assert '30' in out

    def test_format_long_issue(self):
        short = self.command.format_short_issue(self.issue)
        long = self.command.format_long_issue(self.issue)
        assert short in long

    def test_single_issue(self):
        assert self.command.single_issue(30, self.opts, []) == 0
        assert self.command.single_issue(30, self.opts, ['comments']) == 0
        assert self.command.single_issue(30, self.opts, ['commands']) == 1
