Matchmaking
===========

.. automodule:: matching
    :members:

Models
------

.. automodule:: matching.models
    :members:

Forms
-----

.. automodule:: matching.forms
    :members:

Authorize a user to 'matchmake'
--------------------------

Users will have the ability to matchmake if one of:

1 They have superuser status
2 They are a member of the matchmaker group
3 They have been given specific 'matching|invitation|Can matchmake users' privilege

Via the Admin interface select USERNAME from list in 'Authentication and Authorization › Users' :

1 Tick check box Superuser status
2 Select group 'matchmakers' and add
2 Select User permission 'matching|invitation|Can matchmake users' and add
