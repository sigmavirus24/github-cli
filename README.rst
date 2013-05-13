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

    $ gh help issue
    $ gh help issue.assign
    $ gh help issue.close
    $ gh help issue.comment
    $ gh help issue.comments
    $ gh help issue.create
    $ gh help issue.ls
    $ gh help issue.reopen
    

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
