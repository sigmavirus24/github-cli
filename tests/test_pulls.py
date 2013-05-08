import github3
from gh.commands.pull import PullCommand, tc
from base import BaseTest
from mock import patch, call


class TestPullCommand(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestPullCommand, self).__init__(methodName)
        self.number = 13
        self.pull = github3.pulls.PullRequest(self.json('pull'))
        self.command = PullCommand()
        self.command.repository = ('sigmavirus24', 'github3.py')
        self.opts = self.command.parser.parse_args([])
        self.command.repo = github3.repos.Repository(self.json('repo'))

    def test_format_short_pull(self):
        short = self.command.format_short_pull(self.pull)
        assert tc['bold'] in short
        assert 'sigmavirus24' in short

    def test_get_pull(self):
        with patch.object(self.command.repo, 'pull_request') as pr:
            self.command.get_pull(self.number)
            assert pr.assert_called_once()
            assert call(self.number) in pr.mock_calls
