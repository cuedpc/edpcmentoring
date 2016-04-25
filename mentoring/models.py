from django.conf import settings
from django.db import models

class RelationshipManager(models.Manager):
    def active(self):
        """A query-set of active relationships."""
        return self.filter(is_active=True)

    def inactive(self):
        """A query-set of inactive relationships."""
        return self.filter(is_active=False)

class Relationship(models.Model):
    """
    Records a mentorship relation.

    """
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='mentor_relationships',
        on_delete=models.CASCADE)
    mentee = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='mentee_relationships',
        on_delete=models.CASCADE)

    started_on = models.DateField(auto_now_add=True)
    ended_on = models.DateField(blank=True, null=True)
    ended_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='mentor_relationships_ended',
        blank=True, null=True)

    is_active = models.BooleanField(default=True)

    objects = RelationshipManager()

    def __str__(self):
        return '{} mentoring {}'.format(self.mentor, self.mentee)

class Meeting(models.Model):
    """
    A mentoring meeting.

    The in-database duration is likely to have a ludicrous resolution (maybe
    microsecond) but using a DurationField in this model has the advantage that
    it is exposed as a standard Python timedelta object.

    """
    relationship = models.ForeignKey(Relationship, related_name='meetings')
    held_on = models.DateField()
    approximate_duration = models.DurationField()

    def __str__(self):
        return '{} on {}'.format(self.relationship, self.held_on)

    def get_mentor(self):
        return self.relationship.mentor

    def get_mentee(self):
        return self.relationship.mentee
