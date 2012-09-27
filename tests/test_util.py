from unittest import TestCase
from gh.util import find_git_config, get_repository_tuple
import os
import shutil


class TestUtil(TestCase):
    def setUp(self):
        self.orig = os.path.abspath(os.curdir)
        os.makedirs('proj/.git/')
        os.makedirs('proj/subdir/subdir2/subdir3')
        with open('proj/.git/config', 'w+') as fd:
            fd.writelines(
                    [
                       '[core]',
                       'bare = false',
                       '[remote "origin"]'
                       'url = git@github.com:sigmavirus24/Todo.txt-python.git'
                       ]
                    )

    def tearDown(self):
        os.chdir(self.orig)
        shutil.rmtree('proj')

    def test_find_git_config(self):
        dirs = ['./proj', './proj/subdir', './proj/subdir/subdir2',
                './proj/subdir/subdir2/subdir3']
        dirs = [os.path.abspath(d) for d in dirs]
        path = os.path.join(os.path.abspath(os.curdir), 'proj', '.git',
                'clone')
        for d in dirs:
            os.chdir(d)
            assert find_git_config() == path
            assert os.path.abspath(os.curdir) == d

    def test_get_repository_tuple(self):
        assert ('sigmavirus24', 'Todo.txt-python') == get_repository_tuple()
