from django.db import models
from mentoring.models import MentorshipRelationship

class Meeting(models.Model):
    """
    A mentoring meeting.

    The in-database duration is likely to have a ludicrous resolution (maybe
    microsecond) but using a DurationField in this model has the advantage that
    it is exposed as a standard Python timedelta object.

    """
    relationship = models.ForeignKey(MentorshipRelationship)
    held_on = models.DateField()
    approximate_duration = models.DurationField()
