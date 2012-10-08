from abc import abstractmethod, ABCMeta

commands = {}


class Command(object):
    __metaclass__ = ABCMeta
    name = None
    usage = None

    def __init__(self):
        super(Command, self).__init__()
        assert self.name
        commands[self.name] = self

    def main(self, args, options):
        return NotImplemented

    @abstractmethod
    def run(self, options, args):
        return None
