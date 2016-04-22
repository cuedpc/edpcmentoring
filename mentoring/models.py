from django.contrib.auth.models import User
from django.db import models

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    division = models.CharField(max_length=1)
    arrived_on = models.DateField()
    departed_on = models.DateField(null=True)
    expected_departure_on = models.DateField(null=True)
