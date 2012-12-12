from unittest import TestCase
import os
import sys
import json


class BaseTest(TestCase):
    def setUp(self):
        self.stdout = sys.stdout
        sys.stdout = open(os.devnull, 'r+')

    def tearDown(self):
        sys.stdout.close()
        sys.stdout = self.stdout

    def json(self, name):
        path = os.path.join('tests', 'json', name)

        return json.load(open(path)) if os.path.isfile(path) else {}
