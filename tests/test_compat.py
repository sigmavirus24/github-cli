from unittest import TestCase
from gh.compat import input, ConfigParser
import sys


class TestCompat(TestCase):
    def test_input(self):
        if sys.version_info < (3, 0):
            assert input == raw_input
        else:
            assert input == input

    def test_ConfigParser(self):
        if sys.version_info < (3, 0):
            assert 'ConfigParser' == ConfigParser.__module__
        else:
            assert 'configparser' == ConfigParser.__module__
