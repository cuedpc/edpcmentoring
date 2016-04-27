# Notes for developers

## Getting started with a test database

Clone the repository and ``cd`` to it. The remaining instructions assume the
repository root is the current working directory.

Create a virtualenv:

```console
$ virtualenv -p $(which python2.7) env
$ echo "env" >>.git/info/exclude # To avoid any accidental commits
$ . env/bin/activate
```

Install any requirements:

```console
$ pip install -r requirements.txt -r dev-requirements.txt
```

Perform the initial database migration and populate the database with some fake
data:

```console
$ ./manage.py migrate
$ ./manage.py runscript loadtestfixtures
```

Start a local development server:

```console
$ ./manage.py runserver_plus
```

Open http://127.0.0.1:8000 in your web browser.

## Notes on the test database

* There is one superuser: ``test0001``.
* The users ``test0001`` and ``test0002`` can log into the admin interface.
* Users ``test0001`` to ``test0099`` are members of CUED but not all are
  *active*.
* Users ``test0100`` to ``test0199`` exist in the database but are not CUED
  members.

