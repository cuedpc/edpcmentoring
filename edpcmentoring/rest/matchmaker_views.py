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
#    
#    #attempt to filter by seeking type:
#    def get_queryset(self):
#      queryset = Preferences.objects.all()
#      mentor = self.request.query_params.get('mentor', None)
#      mentee = self.request.query_params.get('mentee', None)
#      """  
#      if mentor then is_seeking_mentor set to true
#      """
#      if mentor is not None:
#          queryset = queryset.filter(is_seeking_mentor=True)
#      """
#      if mentee then is_seeking_mentee set to true
#      """
#      if mentee is not None:
#          queryset = queryset.filter(is_seeking_mentee=True)
#
#      return queryset
