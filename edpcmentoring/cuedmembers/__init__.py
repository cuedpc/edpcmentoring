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

.. autofunction:: cuedmembers.get_member_group

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

Settings
--------

CUED_MEMBERS_GROUP
    String giving the name of the group created or returned by
    :py:func:`get_member_group`.

Management commands
-------------------

Synchronising membership data via CSV files
```````````````````````````````````````````

.. automodule:: cuedmembers.management.commands.importcuedmembers

"""
from django.conf import settings

default_app_config = 'cuedmembers.apps.CuedMembersConfig'

def get_member_group():
    """CUED members who are active are a member of a group. Membership of this
    group is automatic for those members who have
    :py:attr:`is_active` set to ``True`` when imported from CSV via
    :py:func:`.csv.read_members_from_csv`.

    .. note::

        The group membership is *not* automatically updated when :py:meth:`save`
        is called on the :py:class:`.models.Member` model. This is because only
        advanced users who know what they're doing should be fiddling with the
        database model directly!

    By default this group is called "CUED Members" but the name may be
    overridden by setting the :py:data:`.CUED_MEMBERS_GROUP` setting.

    """
    # We need to import Group here since apps won't have been loaded when
    # cuedmembers is first imported.
    from django.contrib.auth.models import Group
    group_name = getattr(settings, 'CUED_MEMBERS_GROUP', 'CUED Members')
    return Group.objects.get_or_create(name=group_name)[0]
