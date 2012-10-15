from unittest import TestCase
import sys
import os


class BaseTest(TestCase):
    def setUp(self):
        self.stdout = sys.stdout
        sys.stdout = open(os.devnull, 'r+')

    def tearDown(self):
        sys.stdout.close()
        sys.stdout = self.stdout
