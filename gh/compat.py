try:
    input = raw_input
except NameError:
    pass


try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser
