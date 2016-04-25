from django.conf import settings
from django.db import models

from django.contrib.auth import get_user_model

class Division(models.Model):
    """
    A division within CUED.

    """
    letter = models.CharField(max_length=1, primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.letter

class ResearchGroup(models.Model):
    """
    A research group in CUED.

    """
    division = models.ForeignKey(Division)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Status(models.Model):
    """
    A member of CUED may have multiple statuses. Each status has a separate
    start and end date.

    The start_on and end_on dates are provided by the Department.

    """
    class Meta:
        verbose_name_plural = "Statuses"

    STAFF = 'S'
    POSTGRAD = 'P'
    VISITOR = 'V'
    STATUSES = ((STAFF, 'Staff'), (POSTGRAD, 'Postgrad'), (VISITOR, 'Visitor'))

    member = models.ForeignKey(
        'Member', on_delete=models.CASCADE, related_name='statuses')
    status = models.CharField(max_length=1, choices=STATUSES)
    start_on = models.DateField()
    end_on = models.DateField()

class MemberManager(models.Manager):
    def get_or_create_by_crsid(self, crsid, first_name=None, last_name=None,
                               email=None, **kwargs):
        """
        Retrieve or create a new member from a crsid. If a corresponding user
        does not exist, it is created. The newly created user has
        set_unusable_password() called on it and is added to the database.

        The first_name, last_name and email parameters are set on the
        corresponding user if non-None *even if the user already exists*.

        """
        u, _ = get_user_model().objects.get_or_create(username=crsid)
        m, m_created = self.get_or_create(user=u, **kwargs)

        # Update user
        if first_name is not None:
            u.first_name = first_name
        if last_name is not None:
            u.last_name = last_name
        if email is not None:
            u.email = email
        u.set_unusable_password()
        u.save()

        return m, m_created

    def active(self):
        """A query-set of active users."""
        return self.filter(is_active=True)

    def inactive(self):
        """A query-set of inactive users."""
        return self.filter(is_active=False)

class Member(models.Model):
    """
    An extension of the standard Django User to indicate that a particular
    user is a member of the Department.

    There is a one-to-one mapping of Users to People however not every User is
    necessarily a Member.

    The "Surname" and "Preferred name" fields from the Department are mapped
    through to the associated User's last_name and first_name. The more formal
    "First names" from the department are stored in this model.

    An "active" member is currently present at CUED.

    Information in this model is expected to be provided by the Department. See
    http://www-itsd.eng.cam.ac.uk/datadownloads/support/div_people.html for some
    discussion of what the fields mean.

    The arrived_on date is provided by the Department but should not be used to
    determine "active" status.

    The last_inactive_on date is the date which the Member last stopped being an
    active Member. An active Member will usually have a last_inactive_on date of
    NULL but if someone leaves the Department and returns they may become active
    despite having a last_inactive_on date.

    The upshot of all this is that is_active is the primary means by which one
    should judge if a Member is currently a member of the Department.

    This model does not include role/course, host/supervisor, room number or
    phone number. The "arrived" flag is folded into the is_active field.

    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='cued_member')
    research_group = models.ForeignKey(ResearchGroup, null=True,
                                       related_name='members')

    is_active = models.BooleanField(default=True)
    last_inactive_on = models.DateField(blank=True, null=True)

    arrived_on = models.DateField(auto_now_add=True)

    first_names = models.CharField(
        max_length=100, default='', blank=True)

    objects = MemberManager()

    @property
    def crsid(self):
        """This member's CRSid. The CRSid is the username of the associated
        user.

        """
        return self.user.username

    def __str__(self):
        return '{} ({})'.format(self.user.get_full_name(), self.crsid)
