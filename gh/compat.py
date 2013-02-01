try:
    input = raw_input
except NameError:
    input = input


try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser  # NOQA

import sys

def fix_encoding(content):
    if sys.version_info < (3, 0):
        return content.encode('ascii', 'replace')
    return content
