"""
HTML forms used by the mentoring frontend.

"""
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field
from django import forms

from matching.models import Preferences
from mentoring.forms import ReportMentorMeetingForm as _RMMForm

from .layout import Submit

def long_label_from_user(user):
    return '{} ({})'.format(user.get_full_name(), user.username)

class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return long_label_from_user(obj)

class HTML5DateInput(forms.DateInput):
    """A version of DateInput which uses the HTML5 date input type."""
    input_type = 'date'

class FrontendFormMixin(object):
    class Meta(object):
        submit_text = 'Submit'

    @property
    def helper(self):
        return self.get_helper()

    def get_helper(self):
        helper = FormHelper(self)
        helper.html5_required = True
        helper.error_text_inline = False
        helper.add_input(
            Submit('submit', self.Meta.submit_text),
        )
        return helper

class MentoringPreferencesForm(forms.ModelForm, FrontendFormMixin):
    class Meta(object):
        submit_text = 'Save preferences'
        model = Preferences
        fields = ['is_seeking_mentor', 'mentor_requirements',
                  'is_seeking_mentee', 'mentee_requirements']
        labels = {
            'is_seeking_mentor': 'I am seeking a mentor',
            'is_seeking_mentee': 'I am willing to have a new mentee',
            'mentor_requirements': 'Special requirements for mentor',
            'mentee_requirements': 'Special requirements for mentee',
        }
        help_texts = {
            'mentor_requirements': (
                'Add any comments you wish the person choosing a mentor for '
                'you to read.'),
            'mentee_requirements': (
                'Add any comments you wish the person choosing a mentee for '
                'you to read.'),
        }

    def get_helper(self):
        helper = super(MentoringPreferencesForm, self).get_helper()

        # Make textarea widgets a little wider
        helper.filter_by_widget(forms.Textarea).wrap(
            Field, css_class='campl-input-xlarge')

        return helper

class ReportMentorMeetingForm(FrontendFormMixin, _RMMForm):
    pass
