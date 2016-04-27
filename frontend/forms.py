from crispy_forms.helper import FormHelper
from django import forms

from .layout import Submit

class MentoringPreferencesForm(forms.Form):
    is_seeking_mentor = forms.BooleanField(
        label='I am seeking a mentor', required=False)

    mentor_requirements = forms.CharField(
        label='Special requirements for mentor',
        help_text=(
            'Add any comments you wish the person choosing a mentor for you to '
            'read.'),
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}))

    is_seeking_mentee = forms.BooleanField(
        label='I am seeking a mentee', required=False)

    mentee_requirements = forms.CharField(
        label='Special requirements for mentee',
        help_text=(
            'Add any comments you wish the person choosing a mentee for you to '
            'read.'),
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}))

    @property
    def helper(self):
        helper = FormHelper(self)
        helper.add_input(
            Submit('submit', 'Save preferences')
        )
        return helper
