from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.MatchmakeView.as_view(), name='matchmake'),
]
