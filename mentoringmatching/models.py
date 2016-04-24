from django.db import models
from annoying.fields import AutoOneToOneField
from cuedmembers.models import Member
from mentoring.models import Relationship

class Preferences(models.Model):
    """
    Records the mentorship opinions of a Member.

    """
    class Meta:
        verbose_name_plural = ' preferences'

    member = AutoOneToOneField(
        Member, on_delete=models.CASCADE,
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

    mentor = models.ForeignKey(Member, related_name='mentor_invitations')
    mentee = models.ForeignKey(Member, related_name='mentee_invitations')

    created_by = models.ForeignKey(
        Member, related_name='invitations_created')
    created_on = models.DateField()

    mentor_response = models.CharField(max_length=1, choices=RESPONSES)
    mentee_response = models.CharField(max_length=1, choices=RESPONSES)

    # Note: English spelling, not American
    cancelled_on = models.DateField(blank=True, null=True)

    relationship = models.OneToOneField(Relationship, blank=True, null=True)
