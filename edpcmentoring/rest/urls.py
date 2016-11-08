from django.conf.urls import url, include
from rest_framework import routers
#from epdcmentoring.rest import views

from . import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, "user")
router.register(r'current', views.MyViewSet, "current")
router.register(r'current_preferences', views.MyPreferencesViewSet, "mypreferences")
#TODO an idea can we constrain these 'proxy' endpoints to an authorised user:
router.register(r'proxy', views.ProxyViewSet, "proxy")
router.register(r'groups', views.GroupViewSet)
router.register(r'relationships', views.RelationshipViewSet)
#mentee viewset
router.register(r'mentees', views.MenteeViewSet, 'mentees')
router.register(r'mentors', views.MentorViewSet, 'mentors')
router.register(r'meetings', views.MeetingViewSet)
router.register(r'preferences', views.PreferencesViewSet)
router.register(r'invitations', views.InvitationViewSet)
#router.register(r'profiles', views.ProfileViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',namespace='rest_framework')),
]

