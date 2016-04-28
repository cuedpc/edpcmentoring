Getting started
===============

This section is intended for developers new to the database who want to get up
and running with a test instance quickly.

Before you start
----------------

You should have done the following things before starting to work on the
database:

1. Get a machine running Unix-like OS or Mac OS X. (It makes life easier in the
   long run when dealing with Python.)
2. Install Python and `virtualenv <https://virtualenv.pypa.io/en/latest/>`_.
3. Work through the `Django tutorial
   <https://docs.djangoproject.com/en/stable/intro/tutorial01/>`_.

Running a test instance with fake data
--------------------------------------

Clone the repository and ``cd`` to it. The remaining instructions assume
the repository root is the current working directory.

Create a virtualenv:

.. code:: console

    $ virtualenv -p $(which python2.7) env
    $ echo "env" >>.git/info/exclude # To avoid any accidental commits
    $ . env/bin/activate

Install the requirements:

.. code:: console

    $ pip install -r requirements.txt -r dev-requirements.txt

.. note::

    The ``requirements.txt`` file lists the Python packages required for
    deployment. The ``dev-requirements.txt`` file lists the Python packages used
    only by developers. For example, the "sphinx" package, which is used to
    generate this documentation, is in the ``dev-requirements.txt`` file since
    it is not required when deploying the database.

Perform the initial database migration and populate the database with
some fake data:

.. code:: console

    $ ./manage.py migrate
    $ ./manage.py runscript loadtestfixtures

Start a local development server:

.. code:: console

    $ ./manage.py runserver_plus

Open http://127.0.0.1:8000 in your web browser. The admin interface is at
http://127.0.0.1:8000/admin.

Notes on the test database
--------------------------

-  There is one superuser: ``test0001``.
-  The users ``test0001`` and ``test0002`` can log into the admin
   interface.
-  Users ``test0001`` to ``test0099`` are members of CUED but not all
   are *active*.
-  Users ``test0100`` to ``test0199`` exist in the database but are not
   CUED members.
