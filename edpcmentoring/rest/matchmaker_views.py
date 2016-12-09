from django.shortcuts import render

# Views for matchmakers.
# They can 
#   list all the members searching
#   list all the pending member requests
#   match members together
#   view meetings undertaken by relationships / via a user  

from django.db.models import Q #import 'or' for query_set filter 

from django.contrib.auth.models import User, Group
from mentoring.models import Relationship, Meeting
from matching.models import Preferences, Invitation

from rest_framework import viewsets
from django.views.decorators.csrf import ensure_csrf_cookie
#from edpcmentoring.rest.serializers import UserSerializer, GroupSerializer
from .matchmaker_serializers import MatchSeekingSerializer, UserSerializer, GroupSerializer, BasicRelationshipSerializer, RelationshipSerializer, MeetingSerializer, PreferencesSerializer, MyInvitationSerializer, InvitationSerializer 

# local permission
from rest.permissions import IsMatchMaker, IsUser, IsMentorMenteeORSuper

# To choose actions for viewset
from rest_framework import viewsets, mixins

from rest.views import SeekingRelationshipViewSet

class SeekingRelationshipViewSet1(SeekingRelationshipViewSet):
    """
    The same access as regular members - we can see all 
    """
    permission_classes = (IsMatchMaker,)
        
    serializer_class = MatchSeekingSerializer # includes number of invites and mentor/mentee relationships


 
class InvitationViewSet(
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    """
    API endpoint that allows Invitations to be viewed or edited.
    """
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer

#    This will be received by the Serializer after seriazer.is_valid check - therefore can not use
#    def perform_create(self, serializer):
#        serializer.save(created_by=self.request.user)

