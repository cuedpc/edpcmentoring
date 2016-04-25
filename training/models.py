from django.db import models
from django.conf import settings

class TrainingEvent(models.Model):
    held_on = models.DateField()
    details_url = models.URLField(blank=True)
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name='training_events')
