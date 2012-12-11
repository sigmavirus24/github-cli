from gh.commands.pulls import PullsCommand, tc
from github3 import pull_request
from base import BaseTest


class TestPullsCommand(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestPullsCommand, self).__init__(methodName)
        self.number = 13
        #self.pull = pull_request('sigmavirus24', 'github3.py', self.number)
        #self.command = PullsCommand()
        #self.command.repository = ('sigmavirus24', 'github3.py')
        #opts = self.command.parser.parse_args([])
        #self.command.get_repo(opts)

    #def test_format_short_pull(self):
    #    short = self.command.format_short_pull(self.pull)
    #    assert tc['bold'] in short
    #    assert 'sigmavirus24' in short

    #def test_get_pull(self):
    #    pull = self.command.get_pull(self.number)
    #    assert pull.id == pull.id
