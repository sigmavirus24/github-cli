from abc import abstractmethod, ABCMeta
from optparse import OptionParser
import sys

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

    @abstractmethod
    def run(self, options, args):
        return None


class CustomOptionParser(OptionParser):
    def __init__(self, *args, **kwargs):
        kwargs.update(add_help_option=False)
        OptionParser.__init__(self, *args, **kwargs)
        self.disable_interspersed_args()
        self.add_option('-h', '--help',
                dest='help',
                action='store_true',
                help='Show help')

        self.add_option('-u', '--basic-auth',
                dest='basic_auth',
                action='store_true',
                default=False,
                help='Force basic authentication')

        self.add_option('-c', '--config',
                dest='config_path',
                type='str',
                default='$HOME/.ghconfig',
                nargs=1)

        self.add_option('-L', '--location-aware',
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
