from abc import abstractmethod, ABCMeta
from optparse import OptionParser
from ConfigParser import ConfigParser
from github3 import GitHub
from getpass import getpass
from gh.util import get_repository_tuple, github_config, input
import sys
import os

commands = {}


class Command(object):
    __metaclass__ = ABCMeta
    name = None
    usage = None
    repository = ()

    def __init__(self):
        super(Command, self).__init__()
        assert self.name
        commands[self.name] = self
        self.gh = GitHub()
        self.parser = CustomOptionParser(usage=self.usage)

    @abstractmethod
    def run(self, options, args):
        return None

    def get_repo(self, options):
        self.repo = None
        if self.repository:
            self.repo = self.gh.repository(*self.repository)

        if not self.repository and options.loc_aware:
            self.repo = self.gh.repository(*get_repository_tuple())

    def login(self):
        config = github_config()
        parser = ConfigParser()
        if os.path.isfile(config) and os.access(config, os.R_OK | os.W_OK):
            parser.readfp(open(config))
            self.gh.login(token=parser.get('github', 'token'))
        else:
            user = ''
            while not user:
                user = input('Username: ')
            pw = ''
            while not pw:
                pw = getpass('Password: ')

            auth = self.gh.authorize(user, pw, ['user', 'repo', 'gist'],
                    'github-cli', 'https://github.com/sigmavirus24/github-cli')
            parser.add_section('github')
            parser.set('github', 'token', auth.token)
            self.gh.login(token=auth.token)
            parser.write(open(config, 'w+'))


class CustomOptionParser(OptionParser):
    def __init__(self, *args, **kwargs):
        kwargs.update(add_help_option=False)
        OptionParser.__init__(self, *args, **kwargs)
        self.disable_interspersed_args()


main_parser = CustomOptionParser('%prog [options] [sub-command(s)]')
main_parser.add_option('-h', '--help',
        dest='help',
        action='store_true',
        help='Show help')

main_parser.add_option('-u', '--basic-auth',
        dest='basic_auth',
        action='store_true',
        default=False,
        help='Force basic authentication')

main_parser.add_option('-c', '--config',
        dest='config_path',
        type='str',
        default='$HOME/.ghconfig',
        nargs=1)

main_parser.add_option('-L', '--location-aware',
        dest='loc_aware',
        action='store_false',
        default=True,
        help='Disable location awareness')


def load_command(name):
    full_name = 'gh.commands.{0}'.format(name)
    if full_name not in sys.modules:
        try:
            __import__(full_name)
        except ImportError:
            pass
