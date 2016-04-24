from annoying.fields import AutoOneToOneField
from django.db import models

from cuedmembers.models import Member

class MentorshipPreferences(models.Model):
    """
    Records the mentorship opinions of a Member.

    """
    class Meta:
        verbose_name_plural = "mentorship preferences"

    member = AutoOneToOneField(
        Member, on_delete=models.CASCADE,
        related_name='mentorship_preferences',
        primary_key=True)
    is_seeking_mentor = models.BooleanField(default=False)
    is_seeking_mentee = models.BooleanField(default=False)
    mentor_requirements = models.TextField(blank=True)
    mentee_requirements = models.TextField(blank=True)

class MentorshipRelationshipManager(models.Manager):
    def active(self):
        """A query-set of active relationships."""
        return self.filter(is_active=True)

    def inactive(self):
        """A query-set of inactive relationships."""
        return self.filter(is_active=False)

class MentorshipRelationship(models.Model):
    """
    Records a mentorship relation.

    """
    mentor = models.ForeignKey(
        Member, related_name='mentor_relationships',
        on_delete=models.CASCADE)
    mentee = models.ForeignKey(
        Member, related_name='mentee_relationships',
        on_delete=models.CASCADE)

    started_on = models.DateField()
    ended_on = models.DateField(blank=True, null=True)
    ended_by = models.ForeignKey(
        Member, related_name='mentor_relationships_ended',
        blank=True, null=True)

    is_active = models.BooleanField()

    objects = MentorshipRelationshipManager()

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

    relationship = models.OneToOneField(
        'MentorshipRelationship', blank=True, null=True)

class Meeting(models.Model):
    """
    A mentor/mentee meeting.

    The in-database duration is likely to have a ludicrous resolution (maybe
    microsecond) but using a DurationField in this model has the advantage that
    it is exposed as a standard Python timedelta object.

    """
    relationship = models.ForeignKey('MentorshipRelationship')
    held_on = models.DateField()
    approximate_duration = models.DurationField()

class TrainingEvent(models.Model):
    held_on = models.DateField()
    details_url = models.URLField(blank=True)
    attendees = models.ManyToManyField(Member)

