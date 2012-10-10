from unittest import TestCase
from gh.util import find_git_config, get_repository_tuple, wrap
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
        os.chdir('proj')

    def tearDown(self):
        os.chdir(self.orig)
        shutil.rmtree('proj')

    def test_find_git_config(self):
        dirs = ['./subdir', './subdir/subdir2', './subdir/subdir2/subdir3']
        dirs = [os.path.abspath(d) for d in dirs]
        path = os.path.join(os.path.abspath(self.orig), 'proj', '.git',
                'config')
        for d in dirs:
            os.chdir(d)
            ret = find_git_config()
            assert path == ret
            assert os.path.abspath(os.curdir) == d

    def test_get_repository_tuple(self):
        ret = get_repository_tuple()
        assert ('sigmavirus24', 'Todo.txt-python') == ret

    def test_wrap(self):
        assert ''.join(wrap('foo')) == 'foo'
        eighty = '-' * 80
        wrapped = '-' * 72 + '\n' + '-' * 8
        assert '\n'.join(wrap(eighty)) == wrapped
