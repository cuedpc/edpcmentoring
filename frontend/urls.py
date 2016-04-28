from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^meetings/mentor/new$', views.ReportMentorMeetingView.as_view(),
        name='report_mentor_meeting'),
]

