import logging

from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from cuedmembers.decorators import member_required

from matching.models import Preferences
from mentoring.models import Relationship

from .forms import MentoringPreferencesForm, ReportMentorMeetingForm
from .queries import select_member_details

logger = logging.getLogger(__name__)

@member_required
def index(request):
    mentees = select_member_details(
        Relationship.objects.mentees_for_user(request.user)).order_by('username')
    mentors = select_member_details(
        Relationship.objects.mentors_for_user(request.user)).order_by('username')

    preferences, _ = Preferences.objects.get_or_create(user=request.user)
    preferences_form = MentoringPreferencesForm({
        'is_seeking_mentor': preferences.is_seeking_mentor,
        'mentor_requirements': preferences.mentor_requirements,
        'is_seeking_mentee': preferences.is_seeking_mentee,
        'mentee_requirements': preferences.mentee_requirements,
    })

    return render(request, 'frontend/index.html', {
        'mentees': mentees, 'mentors': mentors,
        'preferences_form': preferences_form,
    })

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

