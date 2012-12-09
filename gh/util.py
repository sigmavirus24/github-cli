from textwrap import TextWrapper
from re import compile
from tempfile import NamedTemporaryFile
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


def trim_numbers(number):
    if number.startswith('#'):
        return number[1:]
    return number


def mktmpfile(prefix='gh-'):
    return NamedTemporaryFile(prefix=prefix, delete=False)


def rmtmpfile(name):
    if name:
        os.remove(name)

# terminal accents
tc = {
    'bold': "\033[1m",
    'default': "\033[0m",
    'underline': "\033[0;4m",
}


def wrap(text):
    if hasattr(wrap, 'tw'):
        tw = wrap.tw
    else:
        tw = TextWrapper(width=72, replace_whitespace=False)

    paragraphs = [p.replace('\n', ' ') for p in text.split('\n\n')]
    paragraphs = ['\n'.join(tw.wrap(p)) for p in paragraphs]
    return '\n\n'.join(paragraphs)


sep = '-' * 78
