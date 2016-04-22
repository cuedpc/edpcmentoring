from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models

@admin.site.register
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
    departed_on = models.DateField(null=True, blank=True)
    expected_departure_on = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user

@admin.site.register
class MentorshipSettings(models.Model):
    """
    Records the mentorship opinions of a StaffMember.

    """
    staff_member = models.OneToOneField('StaffMember', on_delete=models.CASCADE)
    is_seeking_mentor = models.BooleanField()
    is_seeking_mentee = models.BooleanField()

@admin.site.register
class MentorshipRelationships(models.Model):
    """
    Records a mentorship relation.

    """
    mentor_staff_member = models.OneToOneField(
        'StaffMember', related_name='mentees')
    mentee_staff_member = models.OneToOneField(
        'StaffMember', related_name='mentors')

    initiated_by_staff_member = models.OneToOneField(
        'StaffMember', related_name='mentor_relationship_initiated')
    finished_by_staff_member = models.OneToOneField(
        'StaffMember', related_name='mentor_relationship_finished', null=True)

    initiated_on = models.DateField()
    finished_on = models.DateField(null=True, blank=True)
