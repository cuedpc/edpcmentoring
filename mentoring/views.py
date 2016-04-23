from django.shortcuts import render
from .decorators import staff_member_required

@staff_member_required
def index(request):
    return render(request, 'mentoring/index.html')
