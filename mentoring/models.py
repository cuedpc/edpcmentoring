from annoying.fields import AutoOneToOneField
from django.contrib.auth.models import User
from django.db import models

class StaffMemberManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)

class StaffMember(models.Model):
    """
    An extension of the standard Django "User" to indicate that a particular
    user is a member of staff.

    A "current" member of staff is one with no "departed_on" date and with an
    "arrived_on" date in the past. An object manager which operates only on
    current members of staff can be accessed via the "current" attribute.

    The "expected_departure_on" date is based on the staff's contract and is not
    a strong indicator of whether the staff member is "current".

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    division = models.CharField(max_length=1)
    arrived_on = models.DateField()
    departed_on = models.DateField(blank=True, null=True)
    expected_departure_on = models.DateField(blank=True, null=True)
    is_active = models.BooleanField()

    objects = StaffMemberManager()

    def __str__(self):
        return str(self.user)

    def get_mentors(self):
        relationships = self.mentee_relationships.filter(is_active=True)
        return [r.mentor for r in relationships]

    def get_mentees(self):
        relationships = self.mentor_relationships.filter(is_active=True)
        return [r.mentee for r in relationships]

class MentorshipPreferences(models.Model):
    """
    Records the mentorship opinions of a StaffMember.

    """
    class Meta:
        verbose_name_plural = "mentorship preferences"

    staff_member = AutoOneToOneField(
        'StaffMember', on_delete=models.CASCADE,
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
        'StaffMember', related_name='mentor_relationships',
        on_delete=models.CASCADE)
    mentee = models.ForeignKey(
        'StaffMember', related_name='mentee_relationships',
        on_delete=models.CASCADE)

    started_on = models.DateField()
    ended_on = models.DateField(blank=True, null=True)
    ended_by = models.ForeignKey(
        'StaffMember', related_name='mentor_relationships_ended',
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

    mentor = models.ForeignKey('StaffMember', related_name='mentor_invitations')
    mentee = models.ForeignKey('StaffMember', related_name='mentee_invitations')

    created_by = models.ForeignKey(
        'StaffMember', related_name='invitations_created')
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
    The attendance of a StaffMember at a Meeting. The role at the meeting may be
    blank to allow for future mentor/mentee meetings with multiple participants
    but it is expected that this will not be exposed in the UI to begin with.

    """
    MENTOR = 'MR'
    MENTEE = 'ME'
    ROLES = ((MENTOR, 'Mentor'), (MENTEE, 'ME'))

    meeting = models.ForeignKey('Meeting', related_name='attendances')
    attendee = models.ForeignKey('StaffMember')
    role = models.CharField(max_length=1, choices=ROLES)

class TrainingEvent(models.Model):
    held_on = models.DateField()
    details_url = models.URLField(blank=True)
    attendees = models.ManyToManyField('StaffMember')

