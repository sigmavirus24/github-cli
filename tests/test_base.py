from unittest import TestCase
from gh.base import (Command, CustomOptionParser, load_command, commands,
                     main_parser)
import sys


class TestCommand(TestCase):
    def test_run(self):
        class A(Command):
            pass

        try:
            a = A()
            a.run([], [])
        except (TypeError, AssertionError):
            pass


class TestCustomOptionParser(TestCase):
    def test_help(self):
        c = CustomOptionParser()
        assert c.has_option('-h') is True
        assert c.defaults == {'help': False}


class TestBase(TestCase):
    command = 'issue'
    mod = 'gh.commands.issue'

    def setUp(self):
        self.mods = sys.modules.copy()
        if self.mod in sys.modules:
            del sys.modules[self.mod]

        global commands
        if self.command in commands:
            del commands[self.command]

    def tearDown(self):
        sys.modules.update(self.mods)

    def test_load_command(self):
        load_command(self.command)
        assert self.mod in sys.modules
        load_command('foobarbogus')
        assert 'gh.commands.foobarbogus' not in sys.modules

    def test_commands(self):
        assert self.command not in commands
        load_command(self.command)
        error = '{0} not in commands dict'.format(self.command)
        assert self.command in commands, error

    def test_main_parser(self):
        opts, args = main_parser.parse_args(['-h'])
        assert opts.help is True
