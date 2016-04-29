from django.conf import settings
from django.db import models

from django.contrib.auth import get_user_model

class Division(models.Model):
    """
    A division within CUED. The primary key for a division is actually its
    letter, A-F.

    .. attribute:: letter

        The Divisional ID letter, A-F.

    .. attribute:: name

        A human-readable name for the Division.

    """

    letter = models.CharField(max_length=1, primary_key=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.letter

class ResearchGroup(models.Model):
    """
    A research group in CUED.

    .. attribute:: division

        The :py:class:`.Division` which this research group is a part of.

    .. attribute:: name

        A human-readable name for the Research Group.

    """
    division = models.ForeignKey(Division, related_name='research_groups')
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class MemberManager(models.Manager):
    """
    A specialised Manager for :py:class:`.Member` instances.

    """

    def update_or_create_by_crsid(self, crsid, defaults=None):
        """
        Retrieve or create a new member from a crsid. If a corresponding user
        does not exist, it is created. The newly created user has
        set_unusable_password() called on it and is added to the database.

        The first_name, last_name and email entries in defaults are set on the
        corresponding user and any other values are set on the member.

        See the update_or_create() documentation for discussion of the defaults
        parameter.

        """
        defaults = defaults if defaults is not None else {}

        user_keys = set(('first_name', 'last_name', 'email'))
        u_defaults = dict(
            (k, v) for k, v in defaults.items() if k in user_keys)
        m_defaults = dict(
            (k, v) for k, v in defaults.items() if k not in user_keys)
        u, _ = get_user_model().objects.update_or_create(
            username=crsid, defaults=u_defaults)
        u.set_unusable_password()
        u.save()

        m, m_created = self.update_or_create(user=u, defaults=m_defaults)

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

    There is a one-to-one mapping of Users to Members however not every User is
    necessarily a Member.

    .. note::

        While there is nothing stopping you adding a foreign-key to a Member in
        models, its better to add a foreign-key to a User. That way you app's
        models are decoupled from relying on the CUED membership database and
        may be of wider user.

    The "Surname" and "Preferred name" fields from the Department are mapped
    through to the associated User's ``last_name`` and ``first_name``. The
    "First names" provided by the Department are stored in this model.

    An "active" member is currently present at CUED.

    Information in this model is expected to be provided by the Department. See
    http://www-itsd.eng.cam.ac.uk/datadownloads/support/div_people.html for some
    discussion of what the fields mean.

    Note that is_active is the primary means by which one should judge if a
    Member is currently a member of the Department.

    This model does not include role/course, host/supervisor, room number or
    phone number. The "arrived" flag is folded into the is_active field.

    .. attribute:: user

        The :py:class:`django.contrib.auth.models.User` associated with this
        Member.

    .. attribute:: first_names

        A string containing the first names for the member supplied by the
        Department. Although it is tempting to use a space as a separator for
        these, that way danger lies!

    .. attribute:: research_group

        The :py:class:`.ResearchGroup` which this member is a part of.

    .. attribute:: is_active

        Members are not usually deleted from the database. Instead they become
        "active" or "inactive". This is to allow for the same person to be
        considered *as* the same person if they leave CUED and then subsequently
        return.

    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='cued_member')
    first_names = models.CharField(max_length=100, default='', blank=True)

    research_group = models.ForeignKey(ResearchGroup, null=True,
                                       related_name='members')

    is_active = models.BooleanField(default=True)

    objects = MemberManager()

    @property
    def crsid(self):
        """This member's CRSid. The CRSid is the username of the associated
        user.

        This property merely returns the ``username`` of the associated User.

        """
        return self.user.username

    def __str__(self):
        return '{} ({})'.format(self.user.get_full_name(), self.crsid)
