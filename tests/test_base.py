from unittest import TestCase
from gh.base import Command, CustomOptionParser, load_command, commands, wrap
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
        assert c.has_option('-h') is False


class TestBase(TestCase):
    command = 'issues'
    mod = 'gh.commands.issues'

    def setUp(self):
        if self.mod in sys.modules:
            del sys.modules[self.mod]

        global commands
        if self.command in commands:
            commands = {}

    def test_load_command(self):
        load_command(self.command)
        assert self.mod in sys.modules
        load_command('foobarbogus')
        assert 'gh.commands.foobarbogus' not in sys.modules

    def test_commands(self):
        assert self.command not in commands
        load_command(self.command)
        assert self.command in commands

    def test_wrap(self):
        assert ''.join(wrap('foo')) == 'foo'
        eighty = '-' * 80
        wrapped = '-' * 72 + '\n' + '-' * 8
        assert '\n'.join(wrap(eighty)) == wrapped
