#!/usr/bin/env python

import sys
import os
from re import compile

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup  # NOQA

if sys.argv[1] in ('submit', 'publish'):
    os.system('python setup.py sdist upload')
    sys.exit()

sysv = sys.version[:3]

packages = ['gh', 'gh.commands']
requires = ['github3.py>=0.2']
pkg_data = {'': ['LICENSE', 'AUTHORS.rst']}
entry_pt = {'console_scripts': ['gh=gh:main', 'gh-{0}=gh:main'.format(sysv)]}
del sysv

__version__ = ''
with open('gh/__init__.py') as fd:
    reg = compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
    for line in fd:
        match = reg.match(line)
        if match:
            __version__ = match.group(1)
            break

if not __version__:
    raise RuntimeError('Cannot find version information')


setup(
    name='gh-cli',
    version=__version__,
    description='Command-line access to GitHub via github3.py',
    long_description='\n\n'.join([open('README.rst').read(),
                                  open('HISTORY.rst').read()]),
    author='Ian Cordasco',
    author_email='graffatcolmingov@gmail.com',
    url='https://github.com/sigmavirus24/github-cli',
    packages=packages,
    package_data=pkg_data,
    include_package_data=True,
    install_requires=requires,
    test_requires=requires,
    test_suite='run_tests.main',
    entry_points=entry_pt,
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Software Development',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
    ]
)
