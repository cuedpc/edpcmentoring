from django.contrib.auth.models import User
from django.db import models

class MemberManager(models.Manager):
    def active(self):
        """A query-set of active users."""
        return self.filter(is_active=True)

    def inactive(self):
        """A query-set of inactive users."""
        return self.filter(is_active=False)

class Member(models.Model):
    """
    An extension of the standard Django "User" to indicate that a particular
    user is a member of the Department.

    There is a one-to-one mapping of Users to People however not every User is
    necessarily a Member.

    An "active" member is currently present at CUED. This usually implies that
    their departed_on date is NULL and their arrived_on date is in the past but
    that is not required. Instead, "active" means that the Member is currently
    included in the daily snapshot of Department members provided by CUED.

    The arrived_on and expected_departure_on dates are provided by the
    department.

    The departed_on date is the date which the Member last stopped being an
    active Member. An active Member will usually have a departed_on date of NULL
    but if someone leaves the Department and returns they may become active
    despite having a departed_on date.

    The upshot of all this is that is_active is the primary means by which one
    should judge if a Member is currently a member of the Department.

    """
    user = models.OneToOneField(User, related_name='cued_member')
    division = models.CharField(max_length=1)
    is_active = models.BooleanField()

    arrived_on = models.DateField()
    departed_on = models.DateField(blank=True, null=True)
    expected_departure_on = models.DateField(blank=True, null=True)

    objects = MemberManager()

    @property
    def crsid(self):
        """This member's CRSid. The CRSid is the username of the associated
        user.

        """
        return self.user.username
