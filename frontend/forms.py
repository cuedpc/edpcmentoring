"""
HTML forms used by the mentoring frontend.

"""

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field
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

        # Make textarea widgets a little wider
        helper.filter_by_widget(forms.Textarea).wrap(
            Field, css_class='campl-input-xlarge')

        helper.add_input(
            Submit('submit', 'Save preferences')
        )
        return helper
