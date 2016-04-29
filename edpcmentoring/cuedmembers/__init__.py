"""
The CUED People database
========================

The :py:mod:`cuedmembers` application contains models and logic to maintain a
shadow copy of a list of CUED members. It augments the builtin
:py:class:`django.contrib.auth.User` model with information about a member of
CUED. This includes:

    * The full list of "first names";
    * Their research group and division (if any); and
    * Whether they are a current member of CUED.

Members
-------

.. autoclass:: cuedmembers.models.Member
    :members:

.. autoclass:: cuedmembers.models.MemberManager
    :members:

Departmental structure
----------------------

The Department is structure into Divisions which comprise separate Research
Groups. The ``cuedmembers`` app ships with a fixture which is automatically
loaded into the database at migrate-time which contains the current Divisions
and Research Groups.

.. autoclass:: cuedmembers.models.Division
    :members:

.. autoclass:: cuedmembers.models.ResearchGroup
    :members:

Management commands
-------------------

Synchronising membership data via CSV files
```````````````````````````````````````````

.. automodule:: cuedmembers.management.commands.importcuedmembers

"""
default_app_config = 'cuedmembers.apps.CuedMembersConfig'
