from django.conf.urls import url, include
from rest_framework import routers
#from epdcmentoring.rest import views

from . import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, "user")
router.register(r'current', views.MyViewSet, "current")
router.register(r'current_preferences', views.MyPreferencesViewSet, "mypreferences")
#TODO an idea can we constrain these 'proxy' endpoints to an authorised user:
# router.register(r'proxy', views.ProxyViewSet, "proxy")
# router.register(r'groups', views.GroupViewSet)
router.register(r'relationships', views.RelationshipViewSet)
router.register(r'basicrel', views.BasicRelationshipViewSet)
router.register(r'seekrel', views.SeekingRelationshipViewSet,"seekrel") #read only
#mentee viewset
router.register(r'mentees', views.MenteeViewSet, 'mentees') #read only
router.register(r'mentors', views.MentorViewSet, 'mentors') #read only
router.register(r'meetings', views.MeetingViewSet) #only post by mentor mentee or super
#router.register(r'preferences', views.PreferencesViewSet) #TODO - access by user or superuser
router.register(r'invitations', views.InvitationViewSet) #Accept by correct user - TODO accept by superuser
router.register(r'myinvitations', views.MyInvitationViewSet,'myinvitations')
#router.register(r'profiles', views.ProfileViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    # TODO do we remove this to prevent api console access?
    url(r'^api-auth/', include('rest_framework.urls',namespace='rest_framework')),
]

