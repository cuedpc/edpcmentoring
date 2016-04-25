from django.shortcuts import render
from cuedmembers.decorators import member_required

@member_required
def index(request):
    return render(request, 'frontend/index.html')
