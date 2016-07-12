from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Invitation

class InvitationResponseForm(forms.ModelForm):
    """
    A form for responding to an invitation.

    Validates that the user responding to the invitation is one of the mentor or
    the mentee and that the invitation is active.

    Example:

    .. code::

        invitation = # ... Retrieve Invitation instance
        f = InvitationResponseForm(
            data={'user': request.user.id, 'response': Invitation.ACCEPT},
            instance=invitation
        )
        f.save()
    """
    class Meta:
        model = Invitation
        fields = []

    #: The database primary key for the user responding to the invitation.
    user = forms.ModelChoiceField(queryset=get_user_model().objects.all())

    #: The response. One of :py:data:`Invitation.ACCEPT` or
    #: :py:data:`Invitation.DECLINE`
    response = forms.ChoiceField(choices=Invitation.RESPONSES)

    def clean(self):
        cleaned_data = super(InvitationResponseForm, self).clean()
        if not self.instance.is_active():
            raise ValidationError('Invitation is inactive')

        response = cleaned_data.get('response')
        user = cleaned_data.get('user')
        if user is not None and response is not None:
            if response == Invitation.ACCEPT:
                self.instance.respond(user, True)
            elif response == Invitation.DECLINE:
                self.instance.respond(user, False)
            else:
                raise ValidationError('Unknown response: %s' % response)

        return cleaned_data

    def clean_user(self):
        invite = self.instance
        user = self.cleaned_data['user']
        if user.id != invite.mentor.id and user.id != invite.mentee_id:
            raise ValidationError('User is not mentor or mentee')
        return user
