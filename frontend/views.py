from django.shortcuts import render
from cuedmembers.decorators import member_required

from mentoring.models import Relationship

@member_required
def index(request):
    mentor_relationships = Relationship.objects.with_mentor(
        request.user).select_related('mentee__cued_member')
    mentees = [r.mentee.cued_member for r in mentor_relationships]

    mentee_relationships = Relationship.objects.with_mentee(
        request.user).select_related('mentor__cued_member')
    mentors = [r.mentor.cued_member for r in mentee_relationships]

    return render(request, 'frontend/index.html', {
        'mentees': mentees, 'mentors': mentors,
    })
