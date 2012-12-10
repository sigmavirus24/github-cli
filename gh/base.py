from abc import abstractmethod, ABCMeta
from optparse import OptionParser
from github3 import GitHub
from getpass import getpass
from gh.util import github_config
from gh.compat import input, ConfigParser
from gh import __version__
import sys
import os

commands = {}


class Command(object):
    __metaclass__ = ABCMeta
    name = None
    usage = None
    repository = ()
    user = ''
    subcommands = {}
    SUCCESS = 0
    FAILURE = 1
    COMMAND_UNKNOWN = 127

    def __init__(self):
        super(Command, self).__init__()
        assert self.name
        commands[self.name] = self
        self.gh = GitHub()
        self.gh.set_user_agent('github-cli/{0} (http://git.io/MEmEmw)'.format(
            __version__
        ))
        self.parser = CustomOptionParser(usage=self.usage)

    @abstractmethod
    def run(self, options, args):
        return self.FAILURE

    def get_repo(self, options):
        self.repo = None
        if self.repository:
            self.repo = self.gh.repository(*self.repository)

        if not (self.repo or options.loc_aware):
            self.parser.error('A repository is required.')

    def get_user(self):
        if not self.user:
            self.login()
            self.user = self.gh.user()

    def login(self):
        # Get the full path to the configuration file
        config = github_config()
        parser = ConfigParser()

        # Check to make sure the file exists and we are allowed to read it
        if os.path.isfile(config) and os.access(config, os.R_OK | os.W_OK):
            parser.readfp(open(config))
            self.gh.login(token=parser.get('github', 'token'))
        else:
        # Either the file didn't exist or we didn't have the correct
        # permissions
            user = ''
            while not user:
                # We will not stop until we are given a username
                user = input('Username: ')

            self.user = user

            pw = ''
            while not pw:
                # Nor will we stop until we're given a password
                pw = getpass('Password: ')

            # Get an authorization for this
            auth = self.gh.authorize(user, pw, ['user', 'repo', 'gist'],
                                     'github-cli',
                                     'http://git.io/MEmEmw'
                                     )
            parser.add_section('github')
            parser.set('github', 'token', auth.token)
            self.gh.login(token=auth.token)
            parser.write(open(config, 'w+'))

    def help(self):
        self.parser.print_help()
        if self.subcommands:
            print('\nSubcommands:')
            for command in sorted(self.subcommands.keys()):
                print('  {0}:\n\t{1}'.format(
                    command, self.subcommands[command]
                ))
        sys.exit(0)


class CustomOptionParser(OptionParser):
    def __init__(self, *args, **kwargs):
        kwargs.update(add_help_option=False)
        OptionParser.__init__(self, *args, **kwargs)
        self.disable_interspersed_args()
        self.add_option('-h', '--help',
                        dest='help',
                        action='store_true',
                        help='Show help',
                        default=False,
                        )


main_parser = CustomOptionParser('%prog [options] [sub-command(s)]')

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
