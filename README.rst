github-cli
==========

.. image::
    https://secure.travis-ci.org/sigmavirus24/github-cli.png?branch=master
    :alt: Build Status
    :target: http://travis-ci.org/sigmavirus24/github-cli

Currently, this is just an idea, but this tool will provide comprehensive 
interaction with GitHub from the commandline via the API.

Dependencies
------------

- github3.py_

- requests_ (required for github3.py)

Design
------

Take a look at design.rst_\ .

Current Usage
-------------

This shouldn't be installed yet. If you're interested in playing with this, 
however, make sure you have github3.py_ installed. You can then run 
``test.py`` in the root directory. The script is already location aware, but 
you won't see any for this repository (yet). An couple example usages are:

::

    python test.py kennethreitz/requests issues -d asc
    python test.py kennethreitz/requests issues 889 comments
    python test.py kennethreitz/requests issues "#889" comments
    python test.py kennethreitz/requests issues -s closed -n 10 -d asc

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
