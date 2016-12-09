from annoying.fields import AutoOneToOneField
from django.conf import settings
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.timezone import now
from mentoring.models import Relationship
#from rest.models import Profile 

class Preferences(models.Model):
    """
    Records the mentorship opinions of a User.

    """
    class Meta(object):
        verbose_name_plural = 'Preferences'

    user = AutoOneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='mentorship_preferences',
        primary_key=True)
#    profile = AutoOneToOneField(
#        Profile, on_delete=models.CASCADE,
#        related_name='preferences_profile',
#        primary_key=True)
    is_seeking_mentor = models.BooleanField(default=False)
    is_seeking_mentee = models.BooleanField(default=False)
    mentor_requirements = models.TextField(blank=True)
    mentee_requirements = models.TextField(blank=True)

class InvitationManager(models.Manager):
    """
    Model manager for :py:class:`.Invitation` model.

    """
    def active(self):
        """Return a query set giving only the active invitations."""
        return self.filter(deactivated_on__isnull=True)

class Invitation(models.Model):
    """
    An invitation to form a mentoring relationship.

    Invites are the mechanism where mentor/mentee relationships are created. The
    :py:meth:`.clean` method of this model is overridden to allow invites to be
    created by anyone but, in that case, they need to be the mentor or mentee of
    the invite. Users with the "add_invitation" permission can invite any two
    users to form a mentor/mentee relationship.

    Each invitation records who the mentor and mentee are to be and the user who
    created the invite. (This is useful to determine which of the mentors and
    mentees should actually be notified.) The creation date is also stored to
    allow for some form of automatic expiry.

    An "active" invite is one which is not expired and is still awaiting a
    response from the mentor or mentee. An invitation which is declined by
    either mentor or mentee should be marked as inactive even if the other party
    has not responded.

    The :py:attr:`.deactivated_on` date records when this invite became inactive
    either through being declined by one party, accepted by both or manually
    deactivated.

    Should the invite result in a new relationship, this is recorded in the
    :py:attr:`.created_relationship` field.

    """
    ACCEPT = 'A'
    DECLINE = 'D'

    objects = InvitationManager()

    class Meta:
        permissions = (
            ("matchmake", "Can matchmake users"),
        )

    #: The possible responses to an invitation.
    RESPONSES = ((ACCEPT, 'Accept'), (DECLINE, 'Decline'))

    #: The proposed mentor for this relationship
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='mentor_invitations')
    #: The proposed mentee for this relationship
    mentee = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='mentee_invitations')

    #: The User who created this invitation
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='created_invitations')
    #: The date this invitation was created
    created_on = models.DateField(auto_now_add=True)

    #: The response from the mentor to the invite
    mentor_response = models.CharField(max_length=1, choices=RESPONSES,
                                       blank=True)
    #: The response from the mentee to the invite
    mentee_response = models.CharField(max_length=1, choices=RESPONSES,
                                       blank=True)

    #: If inactive, when did this invite become so
    deactivated_on = models.DateField(blank=True, null=True)

    #: If this invite lead to a mentoring relationship, it is recorded here
    created_relationship = models.ForeignKey(
        Relationship, blank=True, null=True,
        related_name='started_by_invitations')

    def respond(self, user, accepted):
        """
        Set the response of the specified user. 
        Unless the user has 'matchmake' and the user is neither the
        mentor or mentee then a PermissionDenied exception is raised.

	If the user is a matchmake then the inivtaton is stolen 
	and both responses are set to the one chosen by the user
        """
        response = Invitation.ACCEPT if accepted else Invitation.DECLINE
        if  user.has_perm('matchmake'): # first so that matchmakers can match their own!
            self.mentee_response = response
            self.mentor_response = response
        elif user.id == self.mentor.id:
            self.mentor_response = response
        elif user.id == self.mentee.id:
            self.mentee_response = response
        else:
            raise PermissionDenied('User is neither mentor or mentee')

        # Either mentor or mentee declining deactivates the invite
        if not accepted:
            self.deactivate()

    def deactivate(self):
        """
        Deactivate this invite without creating a relationship.

        Does nothing if the invite is already deactivated.

        """
        if self.deactivated_on is None:
            self.deactivated_on = now().date()

    def both_willing(self):
        """
        Extra validation checks that both mentor and mentee are willing
        """
        
        mentor_willing = self.mentor.mentorship_preferences.is_seeking_mentee
        mentee_seeking = self.mentee.mentorship_preferences.is_seeking_mentor
        if not mentor_willing or not mentee_seeking:
            raise ValidationError('Mentor '+str(mentor_willing)+' and Mentee '+str(mentee_seeking)+' must be seeking') 
            return False

        return True 


    def clean(self):
        """
        Extra validation for invitations.

        Creating invitations when the creator is not the mentor or mentee
        requires that the creator have the "add_invitation" permission.

        """
        # Check that either a) the creator of the invitation is one of the
        # mentor or mentee or b) that the creator has the required permission.
        creator_is_matchmaker = self.created_by.has_perm('matching.add_invitation')
        creator_is_mentor = self.mentor.id == self.created_by.id
        creator_is_mentee = self.mentee.id == self.created_by.id
        creator_is_mentor_or_mentee = creator_is_mentor or creator_is_mentee
        if not creator_is_matchmaker and not creator_is_mentor_or_mentee:
            raise ValidationError('Creator must be one of the mentor or mentee')

        if (self.mentor.id ==  self.mentee.id):
            raise ValidationError('Mentor can not be Mentee')
 

        # If the creator is one of mentor or mentee, they are assumed to have
        # accepted the invite
        if creator_is_mentor:
            self.mentor_response = Invitation.ACCEPT
        if creator_is_mentee:
            self.mentee_response = Invitation.ACCEPT

        # defer to base class
        return super(Invitation, self).clean()

    def is_accepted(self):
        """
        Returns `True` if both the mentee and mentor have accepted the
        invite.

        """
        mentor_accepted = self.mentor_response == Invitation.ACCEPT
        mentee_accepted = self.mentee_response == Invitation.ACCEPT
        return mentor_accepted and mentee_accepted

    def is_active(self):
        """Returns `True` iff the invite is active (i.e. the "deactivated_on"
        date is blank).

        """
        return self.deactivated_on is None

@receiver(pre_save, sender=Invitation, dispatch_uid='invitation_relationships')
def invitation_create_relationships(instance, **_):
    """
    A pre-save hook for Invitation instances which creates a mentoring
    relationship if:

    * The invitation is accepted
    * The invitation is active
    * There is no current relationship

    """
    # Invites must be active and accepted
    if not instance.is_active() or not instance.is_accepted():
        return

    # Invites must not have an existing relationship
    if instance.created_relationship is not None:
        return

    #TODO place the bottom two queries (+save invite) in a transaction -HELP

    # OK, create the relationship and de-activate the invite
    # TODO we should call clean on our relationship eg to prevent mentor = mentee
    instance.created_relationship = Relationship.objects.create(
        mentor=instance.mentor, mentee=instance.mentee)
    instance.deactivated_on = now().date()

    # Deactive any other matching invites
    Invitation.objects.filter(mentor=instance.mentor,mentee=instance.mentee,deactivated_on__isnull=True).update(deactivated_on=now().date())
