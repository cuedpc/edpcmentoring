from django.db import models
from mentoring.models import Relationship

class Meeting(models.Model):
    """
    A mentoring meeting.

    The in-database duration is likely to have a ludicrous resolution (maybe
    microsecond) but using a DurationField in this model has the advantage that
    it is exposed as a standard Python timedelta object.

    """
    relationship = models.ForeignKey(Relationship)
    held_on = models.DateField()
    approximate_duration = models.DurationField()

    def __str__(self):
        return '{} on {}'.format(self.relationship, self.held_on)

    def get_mentor(self):
        return self.relationship.mentor

    def get_mentee(self):
        return self.relationship.mentee
