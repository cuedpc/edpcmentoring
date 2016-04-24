from django.db import models
from django.contrib.auth.models import User
from annoying.fields import AutoOneToOneField
from mentoring.models import Relationship

class Preferences(models.Model):
    """
    Records the mentorship opinions of a User.

    """
    class Meta:
        verbose_name_plural = 'Preferences'

    user = AutoOneToOneField(
        User, on_delete=models.CASCADE,
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
    # The possible responses to an invitation.
    ACCEPT = 'A'
    DECLINE = 'D'
    RESPONSES = ((ACCEPT, 'Accept'), (DECLINE, 'Decline'))

    mentor = models.ForeignKey(User, related_name='mentor_invitations')
    mentee = models.ForeignKey(User, related_name='mentee_invitations')

    created_by = models.ForeignKey(
        User, related_name='created_invitations')
    created_on = models.DateField()

    mentor_response = models.CharField(max_length=1, choices=RESPONSES)
    mentee_response = models.CharField(max_length=1, choices=RESPONSES)

    is_active = models.BooleanField(default=True)

    # Note: English spelling, not American
    cancelled_on = models.DateField(blank=True, null=True)

    relationship_started = models.ForeignKey(
        Relationship, blank=True, null=True,
        related_name='started_by_invitations')
