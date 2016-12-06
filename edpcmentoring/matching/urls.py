from django.conf.urls import url

from . import views

urlpatterns = [
    #url(r'^$', views.MatchmakeView2.as_view(), name='matchmake'),
    url(r'^$', views.matchmake, name='matchmake'),
]
