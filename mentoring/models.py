from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models

class StaffMember(models.Model):
    """
    An extension of the standard Django "User" to indicate that a particular
    user is a member of staff.

    A "current" member of staff is one with no "departed_on" date and with an
    "arrived_on" date in the past.

    The "expected_departure_on" date is based on the staff's contract and is not
    a strong indicator of whether the staff member is "current".

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    division = models.CharField(max_length=1)
    arrived_on = models.DateField()
    departed_on = models.DateField(blank=True, null=True)
    expected_departure_on = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.user)

admin.site.register(StaffMember)

class MentorshipPreferences(models.Model):
    """
    Records the mentorship opinions of a StaffMember.

    """
    class Meta:
        verbose_name_plural = "mentorship preferences"

    staff_member = models.OneToOneField(
        'StaffMember', on_delete=models.CASCADE)
    is_seeking_mentor = models.BooleanField()
    is_seeking_mentee = models.BooleanField()
    mentor_requirements = models.TextField(blank=True)
    mentee_requirements = models.TextField(blank=True)

admin.site.register(MentorshipPreferences)

class MentorshipRelationship(models.Model):
    """
    Records a mentorship relation.

    """
    mentor = models.ForeignKey('StaffMember', related_name='mentees')
    mentee = models.ForeignKey('StaffMember', related_name='mentors')

    started_on = models.DateField()
    ended_on = models.DateField(blank=True, null=True)
    ended_by = models.ForeignKey(
        'StaffMember', related_name='mentor_relationships_ended',
        blank=True, null=True)

admin.site.register(MentorshipRelationship)

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

admin.site.register(Invitation)

class Meeting(models.Model):
    """
    A mentor/mentee meeting.

    The in-database duration is likely to have a ludicrous resolution (maybe
    microsecond) but using a DurationField in this model has the advantage that
    it is exposed as a standard Python timedelta object.

    """
    held_on = models.DateField()
    approximate_duration = models.DurationField()

admin.site.register(Meeting)

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

admin.site.register(MeetingAttendance)

class TrainingEvent(models.Model):
    held_on = models.DateField()
    details_url = models.URLField(blank=True)
    attendees = models.ManyToManyField('StaffMember')

admin.site.register(TrainingEvent)

