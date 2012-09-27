from re import compile
from collections import namedtuple
import os

repo = namedtuple('Repository', ['owner', 'repo'])


def get_repository_tuple():
    """Parse the git config file for this repository if it exists.

    :returns: namedtuple with attributes, owner and repo
    """
    # If there are multiple remotes, this could choose the wrong one
    reg = compile(
            '(?:https://|git@)github\.com(?::|/)([^\./-]*)/(.*)'
            )
    config = find_git_config()
    if not config:
        return ()

    fd = open(config)
    r = repo('', '')
    for line in fd:
        match = reg.search(line)
        if match and match.groups():
            r = repo(*match.groups())
            break

    fd.close()
    if r.repo.endswith('.git'):
        r = repo(r.owner, r.repo[:-4])
    return r


def find_git_config():
    """Attempt to find the git config file for this repository in this
    directory and it's parent.
    """
    # Not generic, needs to be generalized
    current_dir = os.path.abspath('.git')
    current_config = os.path.abspath('.git/config')
    parent_dir = os.path.abspath('../.git')
    parent_config = os.path.abspath('../.git/config')

    if os.lstat(current_dir) and os.access(current_config, os.R_OK):
        return current_config
    if os.lstat(parent_dir) and os.access(parent_config, os.R_OK):
        return parent_config
    return ''
