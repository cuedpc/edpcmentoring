from annoying.fields import AutoOneToOneField
from django.conf import settings
from django.db import models
from mentoring.models import Relationship

class Preferences(models.Model):
    """
    Records the mentorship opinions of a User.

    """
    class Meta(object):
        verbose_name_plural = 'Preferences'

    user = AutoOneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='mentorship_preferences',
        primary_key=True)
    is_seeking_mentor = models.BooleanField(default=False)
    is_seeking_mentee = models.BooleanField(default=False)
    mentor_requirements = models.TextField(blank=True)
    mentee_requirements = models.TextField(blank=True)

class Invitation(models.Model):
    """
    An invitation to form a mentoring relationship.

    Invites are the mechanism where mentor/mentee relationships are created. An
    invite can be created by anyone but, in that case, they need to be the
    mentor or mentee of the invite. Users with the "matchmake" permission can
    invite any two users to form a mentor/mentee relationship.

    Each invitation records who the mentor and mentee are to be and the user who
    created the invite. (This is useful to determine which of the mentors and
    mentees should actually be notified.) The creation date is also stored to
    allow for some form of automatic expiry.

    An "active" invite is one which is not expired and is still awaiting a
    response from the mentor or mentee. An invitation which is declined by
    either mentor or mentee is marked as inactive even if the other party has
    not responded. The :py:attr:`.deactivated_on` date records when this invite
    became inactive either through being declined by one party or accepted by
    both.

    Should the invite result in a new relationship, this is recorded in the
    :py:attr:`.created_relationship` field.

    .. attribute:: mentor

        The user who is to be the mentor.

    .. attribute:: mentee

        The user who is to be the mentee.

    """
    class Meta(object):
        permissions = (
            ('matchmake', 'Can matchmake mentors and mentees with each other'),
        )

    # The possible responses to an invitation.
    ACCEPT = 'A'
    DECLINE = 'D'
    RESPONSES = ((ACCEPT, 'Accept'), (DECLINE, 'Decline'))

    mentor = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='mentor_invitations')
    mentee = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='mentee_invitations')

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='created_invitations')
    created_on = models.DateField(auto_now_add=True)

    mentor_response = models.CharField(max_length=1, choices=RESPONSES)
    mentee_response = models.CharField(max_length=1, choices=RESPONSES)

    is_active = models.BooleanField(default=True)
    deactivated_on = models.DateField(blank=True, null=True)

    created_relationship = models.ForeignKey(
        Relationship, blank=True, null=True,
        related_name='started_by_invitations')
