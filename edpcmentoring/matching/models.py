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

    """
    class Meta(object):
        permissions = (
            ('matchmake', 'Can matchmake mentors and mentees'),
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

    # Note: English spelling, not American
    cancelled_on = models.DateField(blank=True, null=True)

    relationship_started = models.ForeignKey(
        Relationship, blank=True, null=True,
        related_name='started_by_invitations')
