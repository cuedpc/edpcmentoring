import logging

from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic.edit import FormView, UpdateView
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from cuedmembers.decorators import member_required

from mentoring.models import Relationship

from .forms import ReportMentorMeetingForm, MentoringPreferencesForm
from .queries import select_member_details

logger = logging.getLogger(__name__)

@member_required
def index(request):
    mentees = select_member_details(
        Relationship.objects.mentees_for_user(request.user)).order_by('username')
    mentors = select_member_details(
        Relationship.objects.mentors_for_user(request.user)).order_by('username')

    preferences = request.user.mentorship_preferences

    return render(request, 'frontend/index_2col.html', {
        'mentees': mentees, 'mentors': mentors,
        'preferences': preferences,
    })

class MentoringPreferencesView(UpdateView):
    form_class = MentoringPreferencesForm
    template_name = 'frontend/mentoring_preferences_form.html'

    @method_decorator(member_required)
    def dispatch(self, request, *args, **kwargs):
        # Guaranteed by member_required
        assert request.user.cued_member is not None
        return super(MentoringPreferencesView, self).dispatch(
            request, *args, **kwargs
        )

    def get_object(self, queryset=None):
        return self.request.user.mentorship_preferences

    def get_success_url(self):
        return reverse('index')

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, 'Your preferences have been saved.')
        return super(MentoringPreferencesView, self).form_valid(form)

class ReportMentorMeetingView(FormView):
    form_class = ReportMentorMeetingForm
    template_name = 'frontend/mentor_meeting_form.html'

    def __init__(self, *args, **kwargs):
        super(ReportMentorMeetingView, self).__init__(*args, **kwargs)
        self._request_user = None

    @method_decorator(member_required)
    def dispatch(self, request, *args, **kwargs):
        # Guaranteed by member_required
        assert request.user.cued_member is not None

        # Record the requesting user
        try:
            self._request_user = request.user
            return super(ReportMentorMeetingView, self).dispatch(
                request, *args, **kwargs
            )
        finally:
            self._request_user = None

    def form_valid(self, form):
        """Save the meeting to the DB and redirect."""
        form.save()
        messages.add_message(
            self.request, messages.INFO, 'Your meeting has been recorded.')
        return super(ReportMentorMeetingView, self).form_valid(form)

    def get_initial(self):
        initial = super(ReportMentorMeetingView, self).get_initial()
        initial['held_on'] = timezone.now()
        return initial

    def get_form_kwargs(self):
        kwargs = super(ReportMentorMeetingView, self).get_form_kwargs()
        kwargs['mentor'] = self._request_user
        return kwargs

    def get_success_url(self):
        return reverse('index')

