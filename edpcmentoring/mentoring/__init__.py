"""
Mentoring relationships
=======================

The :py:mod:`mentoring` application provides the core of the
mentorship management support.

Relationships
-------------

.. autoclass:: mentoring.models.Relationship
    :members:

.. autoclass:: mentoring.models.RelationshipManager
    :members:

Meetings
--------

.. autoclass:: mentoring.models.Meeting
    :members:

.. autoclass:: mentoring.forms.ReportMentorMeetingForm
    :members:

"""

default_app_config = 'mentoring.apps.MentoringConfig'

