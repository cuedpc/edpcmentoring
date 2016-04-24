from django.db import models
from cuedmembers.models import Member

class TrainingEvent(models.Model):
    held_on = models.DateField()
    details_url = models.URLField(blank=True)
    attendees = models.ManyToManyField(Member)
