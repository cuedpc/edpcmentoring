from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

class RelationshipManager(models.Manager):
    def active(self):
        """A queryset of active relationships."""
        return self.filter(is_active=True)

    def inactive(self):
        """A queryset of inactive relationships."""
        return self.filter(is_active=False)

    def mentees_for_user(self, user):
        """A queryset returning all users who are the passed user's mentees.
        Only active relationships are considered.

        """
        return get_user_model().objects.filter(
            mentee_relationships__mentor=user,
            mentee_relationships__is_active=True)

    def mentors_for_user(self, user):
        """A queryset returning all users who are the passed user's mentors.
        Only active relationships are considered.

        """
        return get_user_model().objects.filter(
            mentor_relationships__mentee=user,
            mentor_relationships__is_active=True)

class Relationship(models.Model):
    """
    The mentoring database is structured around the concept of a "mentoring
    relationship" between two users. One user will be the mentor and one will be
    the mentee.

    .. note::

        This model is not yet completely set in stone. In particular, it's
        unclear whether the ending of the relationship should be recorded in the
        model or in a related model.

    .. attribute:: mentor

        The user who is the mentor in this relationship.

    .. attribute:: mentee

        The user who is the mentee in this relationship.

    .. attribute:: is_active

        True iff this relationship is currently active.

    """
    class Meta(object):
        unique_together = (('mentor', 'mentee'),)

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

    def clean(self):
        super(Relationship, self).clean()
        if self.mentor.id == self.mentee.id:
            raise ValidationError('Cannot have the same user, %(user)s, as '
                                  'both mentor and mentee',
                                  params={'user':str(self.mentor)})


    def end(self,user):
        """
        End this relationship.
        
        """
        if self.ended_on is None:
            self.ended_on = now().date()
	    self.ended_by = user

class Meeting(models.Model):
    """
    Meetings are recorded for a particular relationship.

    .. note::

        The in-database duration is likely to have a ludicrous resolution (maybe
        microsecond) but using a DurationField in this model has the advantage
        that it is exposed as a standard Python timedelta object.

    .. note::

        It is likely that a "happened" field will need to be added to this model
        at some point to allow users to specify that a meeting was mistakenly
        recorded.

    .. attribute:: relationship

        The :py:class:`.Relationship` this meeting is associated with.

    .. attribute:: held_on

        The date this meeting was held.

    .. attribute:: approximate_duration

        The approximate duration of the meeting.

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
