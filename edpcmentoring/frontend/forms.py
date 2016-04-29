"""
HTML forms used by the mentoring frontend.

"""
from datetime import timedelta

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field
from django import forms
from django.db import transaction
from django.core.exceptions import ValidationError

from matching.models import Preferences
from mentoring.models import Relationship, Meeting

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

class ReportMentorMeetingForm(forms.Form, FrontendFormMixin):
    class Meta(object):
        submit_text = 'Record meeting'

    # The mentor field is ignored but is included here to reassure the user that
    # they are indeed doing the right thing.
    mentor = forms.CharField(disabled=True, required=False)
    mentee = UserChoiceField(queryset=None)
    held_on = forms.DateField(widget=HTML5DateInput)
    duration = forms.IntegerField(
        label='Approximate duration in minutes',
        min_value=1, max_value=3600, initial=30)

    def __init__(self, *args, **kwargs):
        self._mentor_user = kwargs.pop('mentor', None)
        super(ReportMentorMeetingForm, self).__init__(*args, **kwargs)
        self.fields['mentee'].queryset = \
            Relationship.objects.mentees_for_user(self._mentor_user)
        if self._mentor_user is not None:
            self.fields['mentor'].initial = long_label_from_user(self._mentor_user)

    def clean(self):
        cleaned_data = super(ReportMentorMeetingForm, self).clean()

        if self._mentor_user is None:
            raise ValidationError('A mentor must be specified',
                                  code='missing_mentor')

        # Ensure that there's not an existing meeting on this date. This is
        # UI-level validation rather than a uniqueness constraint in the DB.
        # (The check is intended to guard against double-reporting of a meeting
        # rather than a loss of DB consistency.)
        qs = Meeting.objects.filter(
            held_on=cleaned_data.get('held_on'),
            relationship__mentor=self._mentor_user,
            relationship__mentee=cleaned_data.get('mentee'),
        )
        if qs.exists():
            raise ValidationError(
                ('A meeting between %(mentor)s and %(mentee)s on %(date)s '
                 'has already been recorded.'),
                code='duplicate_meeting',
                params={
                    'mentor': long_label_from_user(self._mentor_user),
                    'mentee': long_label_from_user(cleaned_data.get('mentee')),
                    'date': cleaned_data.get('held_on').isoformat(),
                })

        return cleaned_data

    @transaction.atomic
    def save(self):
        """Save this meeting to the DB."""
        relationship = Relationship.objects.get(
            mentor=self._mentor_user, mentee=self.cleaned_data['mentee'])
        Meeting.objects.update_or_create(
            relationship=relationship, held_on=self.cleaned_data['held_on'],
            approximate_duration=timedelta(minutes=self.cleaned_data['duration']),
        )
