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
    held_on = models.DateField()
    approximate_duration = models.DurationField()

class MeetingAttendance(models.Model):
    """
    The attendance of a Member at a Meeting. The role at the meeting may be
    blank to allow for future mentor/mentee meetings with multiple participants
    but it is expected that this will not be exposed in the UI to begin with.

    """
    MENTOR = 'MR'
    MENTEE = 'ME'
    ROLES = ((MENTOR, 'Mentor'), (MENTEE, 'ME'))

    meeting = models.ForeignKey('Meeting', related_name='attendances')
    attendee = models.ForeignKey(Member)
    role = models.CharField(max_length=1, choices=ROLES)

class TrainingEvent(models.Model):
    held_on = models.DateField()
    details_url = models.URLField(blank=True)
    attendees = models.ManyToManyField(Member)

