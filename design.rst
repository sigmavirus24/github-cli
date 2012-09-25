Functionality
=============

In the examples below, I preceed examples with a repo name. This implies that 
they're owned by the authenticated user. It would be wonderful if like octogit
gh could become location aware, e.g., if I'm in ``~/sandbox/github3.py``, I 
wouldn't need to specify it. Taking the argument, however, allows a user to 
specify any repository they want from anywhere on their machine.

- Manage issues

  + List issues on a repository or collection of repositories

    ::

        $ gh github3.py list issues
         4 Serialization of Objects (@sigmavirus24)
        15 Pagination of certain functions (@sigmavirus24)
        16 Fix usage of expect.raises (@sigmavirus24)
        17 TypeError exception when trying to create an existing repo 
           `Org.create_repo` (@sethwoodworth)
        $ gh github3.py list issues [closed|all]

  + Display info of an issue

    ::

        $ gh github3.py issue 15
        Pagination of certain functions (@sigmavirus24)
        -----------------------------------------------------------------------
        So currently, when someone uses a method like ``list_issues()`` they 
        only get the first "page" of issues as returned by the API (provided 
        the parameters they decide to use). The next "page" can be accessed by 
        appending ``page=2`` or by accessing the link headers of the response 
        object and using ``rel_next`` but not through the ``list_issues()`` 
        method.

        The first option that came to mind was accepting another parameter to  
        ``list_issues()``: ``page``. ``page`` would accept any of the 
        following: ``rel_next``, ``rel_prev``, ``rel_first``, ``rel_last``, 
        and ``<int>``. The problem then occurs, of course when someone does 
        something like

        ```python
        from github3 import repository
        
        repo = repository(owner, repo_name)
        issues = repo.list_issues(page='rel_next')
        ```````

        There is no current set of link headers for this so ``rel_next`` would 
        not produce obvious results. To try and guess what the user meant 
        would be  ridiculous, so the obvious solution would be to just return 
        the first page. If  they give us an integer, then clearly they just 
        want that one page and we add that as a parameter (easy).

        The next option that came to mind was to change ``list_issues()`` to 
        list **all** issues on a repository and to introduce a function 
        ``iter_issues()`` which yields each page as a list of ``Issue``s. The 
        problem with this then occurs that you can not request a specific page 
        unless we use yet another function.

        So right now I think the first option would be the least confusing of 
        the two options but with an extra acceptable value for ``page`` -- 
        "all". Any and all input is very welcome.

  + List/create comments on an issue

  + Close/reopen an issue

  + Add/remove assignees, labels and milestones

- Manage pull requests

  + List pull requests

    ::

        $ gh github3.py list pulls [closed|open|all]

  + Display contents of a pull request

    ::

        $ gh github3.py pull 14

  + List/create comments on a pull request

  + Close/reopen/merge a pull request

- Manage repositories

  + Create new repos easily

    = Even on organizations

  + Display information about existing ones (including other people's repos)

  + I will never allow anyone to delete a repository from the command-line.

  + Star/unstar and subscribe to/unsubscribe from repositories

- Manage gists

  + Create new gists from stdin or a file

  + Delete existing gists

  + Fork gists

  + List personal gists and latest gists.

  + Comment on gists

- List events received by the authenticated user


Design
======

This project will be large enough to warrant a pip like design.

::

    github-cli/
    - setup.py
    - MANIFEST.in
    - .travis.yml
    - docs/
      + # etc.
    - gh/
      + __init__.py
      + main.py
      + commands/
        - __init__.py
        - gist.py
        - issue.py
        - list.py
        - news.py
        - pull.py
        - repo.py
