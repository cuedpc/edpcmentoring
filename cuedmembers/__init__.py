"""
Keeping track of CUED membership
================================

The :py:mod:`cuedmembers` application contains models and logic to maintain a
shadow copy of a list of CUED members.

Departmental structure is recorded through the :py:class:

Models
======

.. autoclass:: cuedmembers.models.Division
    :members:

.. autoclass:: cuedmembers.models.ResearchGroup
    :members:

"""
default_app_config = 'cuedmembers.apps.CuedMembersConfig'
