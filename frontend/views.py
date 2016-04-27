from django.shortcuts import render
from cuedmembers.decorators import member_required

from matching.models import Preferences
from mentoring.models import Relationship

from .forms import MentoringPreferencesForm

@member_required
def index(request):
    mentor_relationships = Relationship.objects.with_mentor(
        request.user).select_related('mentee__cued_member')
    mentees = [r.mentee.cued_member for r in mentor_relationships]

    mentee_relationships = Relationship.objects.with_mentee(
        request.user).select_related('mentor__cued_member')
    mentors = [r.mentor.cued_member for r in mentee_relationships]

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
