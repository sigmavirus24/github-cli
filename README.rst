github-cli
==========

.. image::
    https://secure.travis-ci.org/sigmavirus24/github-cli.png?branch=master
    :alt: Build Status
    :target: http://travis-ci.org/sigmavirus24/github-cli


This tool provides partial interaction with GitHub and its API from the 
command line. This tool is far from complete or comprehensive.

Dependencies
------------

- github3.py_

  + requests_

Current Usage
-------------

If you would like command completion, look in the completion directory for 
your shell of choice. If you don't see one for your shell, feel free to send a 
pull request adding one! **Note**: The current bash completion is imperfect so 
feel free to improve on it and send pull requests.

To get a comprehensive look at the following commands, use their help pages 
like below.

help
~~~~

::

    $ gh help
    # Alternatively gh -h

::

    $ gh help follow
    $ gh help fork
    $ gh help gists
    $ gh help issues
    $ gh help my
    $ gh help pulls
    $ gh help repos
    $ gh help unfollow

create.gist
~~~~~~~~~~~

::

    $ echo "This is stdin" | gh create.gist -
    $ gh create.gist -d "Public gist" file1.rb file2.rb file3.rb
    $ gh create.gist -p -d "Private gist" file1.py file2.py file3.py

create.issue
~~~~~~~~~~~~

::

    $ gh create.issue -t 'New bug found in version 0.10'

create.pull
~~~~~~~~~~~

::

    $ gh create.pull -t 'Fixes issue #50' sigmavirus24:fix50 master
    $ gh create.pull -i 50 sigmavirus24:fix50 master

create.repo
~~~~~~~~~~~

::

    $ gh create.repo awesome_repo
    $ gh create.repo -o orgname awesome_repo

follow
~~~~~~

::

    $ gh follow kennethreitz
    $ gh follow sigmavirus24

fork.gist
~~~~~~~~~

::

    $ gh fork.gist 10

fork.repo
~~~~~~~~~

::

    $ gh fork.repo kennethreitz/requests
    $ gh fork.repo sigmavirus24/github3.py
    $ gh fork.repo sigmavirus24/github-cli

gists
~~~~~

::

    $ gh gists
    $ gh gists -u sigmavirus24

issues
~~~~~~

::

    $ cd path/to/repo/on/GitHub
    $ gh issues
    $ gh -r sigmavirus24/github3.py issues
    $ gh -r sigmavirus24/github3.py issues 48
    $ gh issues 48 close
    $ gh issues 48 reopen
    $ gh issues 48 comment
    $ gh issues 48 comments

my
~~

::

    $ gh my notifications
    $ gh my dashboard
    $ gh my issues
    $ gh my stars
    $ gh my profile

pulls
~~~~~

::

    $ cd path/to/repo/on/GitHub
    $ gh pulls
    $ gh pulls 48 merge
    $ gh pulls 48 close
    $ gh pulls 48 comments

repos
~~~~~

::

    $ gh repos kennethreitz

star
~~~~

::

    $ gh star kennethreitz/tablib
    $ gh star some_repo_i_own

unfollow
~~~~~~~~

::

    $ gh unfollow sigmavirus24

unstar
~~~~~~

::

    $ gh unstar some_repo_i_own
    $ gh unstar sigmavirus24/requests

License
-------

.. image::
    http://gplv3.fsf.org/gplv3-127x51.png
    :alt: GPLv3
    :target: https://github.com/sigmavirus24/github-cli/blob/master/LICENSE


.. links:
.. _github3.py: https://github.com/sigmavirus24/github3.py
.. _requests: https://github.com/kennethreitz/requests
.. _design.rst:
    https://github.com/sigmavirus24/github-cli/blob/master/design.rst
