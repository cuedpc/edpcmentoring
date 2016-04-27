from django.shortcuts import render
from cuedmembers.decorators import member_required

from matching.models import Preferences
from mentoring.models import Relationship

from .forms import MentoringPreferencesForm
from .queries import select_member_details

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
