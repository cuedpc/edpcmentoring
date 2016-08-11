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
    only by developers. For example, the "ipython" package, which is used to
    improve the ``shell_plus`` command, is in the ``dev-requirements.txt`` file
    since it is not required when deploying the database.

Perform the initial database migration and populate the database with
some fake data:

.. code:: console

    $ ./edpcmentoring/manage.py migrate
    $ ./edpcmentoring/manage.py runscript loadtestfixtures

Start a local development server:

.. code:: console

    $ ./edpcmentoring/manage.py runserver_plus

Open http://127.0.0.1:8000 in your web browser. The admin interface is at
http://127.0.0.1:8000/admin.

Installing on UIS MWS3 (https://panel.mws3.csx.cam.ac.uk/)
----------------------------------------------------------

You will need:

- To register and create an MWS3 server (see link above)
- The root passwword for mysql server (available once you MWS3 has been setup)
    
ssh onto you MWS3 server (putty, linu/unix console)

.. code:: console
    $ cd /var/www/default/admindir
    $ git clone https://github.com/cuedpc/edpcmentoring.git
    $ python edpcmentoring/setup_mws.py
    
You will be asked for 

- The server's Mysql root password.
- A short name which will be prefixed by 'pc_' and used as the database name
- A password the django applicatomn will use to connect to the Mysql server
- A unique passphrase, secret key for your application
- Whether you wish to load the sample test data into the application

Once complete you should be able to visit the mws3's host name and if loade the test data login as test000X.

.. note::

    The local config is held in edpcmentoring/edpcmentoring/edpcmentoring/settings_local.py, and DEBUG is set to True - not advised for production systems. 


Notes on the test database
--------------------------

-  There is one superuser: ``test0001``.
-  The users ``test0001`` and ``test0002`` can log into the admin
   interface.
-  Users ``test0001`` to ``test0099`` are members of CUED but not all
   are *active*.
-  Users ``test0100`` to ``test0199`` exist in the database but are not
   CUED members.

Development
-----------

This section contains some important information if you're thinking of
developing a feature for the database.

Tests
'''''

The test suite for the mentoring database is run via the ``tox`` test-runner. If
you're intending to develop a feature for the database, it is important that you
write tests. By default, ``tox`` will run tests using whichever Python version
correspond to the installed ``python`` and ``python3`` binaries.

Install ``tox`` via pip:

.. code:: console

    $ pip install --user tox

You can now run the tests via the ``tox`` command:

.. code:: console

    $ tox

Any positional arguments are passed to the underlying invocation of ``manage.py
test`` and so you can specify a particular application to test by giving it's
directory. For example:

.. code:: console

    $ tox edpcmentoring/cuedmembers

Code coverage
'''''''''''''

The tests are run under the ``coverage`` code-coverage utility and files which
do not have 100% test coverage are printed out after the tests are run.
Additionally, a HTML report is generated in ``htmlcov/`` which is useful for
determining which lines are untested.

Although 100% code coverage is probably infeasible in general, we aim for as
close as possible in the database. Pull requests which increase test code
coverage are welcome.

