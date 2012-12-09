try:
    input = raw_input
except NameError:
    input = input


try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser  # NOQA
