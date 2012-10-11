from textwrap import TextWrapper
from re import compile
import os


def get_repository_tuple():
    """Parse the git config file for this repository if it exists.

    :returns: namedtuple with attributes, owner and repo
    """
    # If there are multiple remotes, this could choose the wrong one
    reg = compile(
            '(?:https://|git@)github\.com(?::|/)([^\./-]*)/(.*)'
            )
    config = find_git_config()
    r = ()
    if config:
        fd = open(config)
        for line in fd:
            match = reg.search(line)
            if match and match.groups():
                r = match.groups()
                break

        fd.close()

    if r and r[1].endswith('.git'):
        r = (r[0], r[1][:-4])
    return r


def find_git_config():
    """Attempt to find the git config file for this repository in this
    directory and it's parent.
    """
    original = cur_dir = os.path.abspath(os.curdir)
    home = os.path.abspath(os.environ.get('HOME', ''))

    while cur_dir != home:
        if os.path.isdir('.git') and os.access('.git/config', os.R_OK):
            os.chdir(original)
            return os.path.join(cur_dir, '.git', 'config')
        else:
            os.chdir(os.pardir)
            cur_dir = os.path.abspath(os.curdir)

    os.chdir(original)
    return ''


def github_config():
    """Attempt to find the github config file."""
    home = os.path.abspath(os.environ.get('HOME', ''))
    config = os.path.join(home, '.githubconfig')
    return config

# terminal accents
tc = {
    'bold': "\033[1m",
    'default': "\033[0m",
    'underline': "\033[0;4m",
    }

wrap = TextWrapper(width=72, replace_whitespace=False).wrap

try:
    input = raw_input
except NameError:
    pass
