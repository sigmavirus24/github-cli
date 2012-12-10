github-cli
==========

![Build Status](https://secure.travis-ci.org/sigmavirus24/github-cli.png?branch=master)
 
This tool provides partial itneraction with GitHub and its API from the 
command line. This tool is far from complete or comprehensive.

Dependencies
------------

- [github3.py](https://github.com/sigmavirus24/github3.py)

- [requests](https://github.com/kennethreitz/requests) (required for 
  github3.py)

Current Usage
-------------

To get a comprehensive look at the following commands, use their help pages 
like below.

help
~~~~


```
$ gh help
# Alternatively gh -h
```


```
$ gh help follow
$ gh help fork
$ gh help gists
$ gh help issues
$ gh help my
$ gh help pulls
$ gh help repos
$ gh help unfollow
```

follow
~~~~~~

```
$ gh follow kennethreitz
$ gh follow sigmavirus24
```

fork
~~~~

```
$ gh fork kennethreitz/requests
$ gh fork sigmavirus24/github3.py
$ gh fork sigmavirus24/github-cli
```

gists
~~~~~

```
$ gh gists
$ gh gists -u sigmavirus24
$ gh gists create -d "Public gist" file1.rb file2.rb file3.rb
$ gh gists create -p -d "Private gist" file1.py file2.py file3.py
```

issues
~~~~~~

```
$ cd path/to/repo/on/GitHub
$ gh issues
$ gh sigmavirus24/github3.py issues
$ gh sigmavirus24/github3.py issues 48
$ gh issues 48 close
$ gh issues 48 reopen
$ gh issues 48 comment
$ gh issues 48 comments
```

my
~~

```
$ gh my notifications
$ gh my dashboard
$ gh my issues
$ gh my stars
$ gh my profile
```

pulls
~~~~~

```
$ cd path/to/repo/on/GitHub
$ gh pulls
$ gh pulls 48 merge
$ gh pulls 48 close
$ gh pulls 48 comments
```

repos
~~~~~

```
$ gh repos
$ gh repos create new_repo
$ gh repos -o orgname create new_repo
```

unfollow
~~~~~~~~

```
$ gh unfollow sigmavirus24
```

Design
------

Take a look at 
[design.rst](https://github.com/sigmavirus24/github-cli/blob/master/design.rst).

License
-------

![GPLv3](http://gplv3.fsf.org/gplv3-127x51.png)

