from django.shortcuts import render

# Create your views here.

from django.db.models import Q #import 'or' for query_set filter 

from django.contrib.auth.models import User, Group
from mentoring.models import Relationship, Meeting
from matching.models import Preferences, Invitation

from rest_framework import viewsets
from django.views.decorators.csrf import ensure_csrf_cookie
#from edpcmentoring.rest.serializers import UserSerializer, GroupSerializer
from .serializers import SeekingSerializer, UserSerializer, GroupSerializer, BasicRelationshipSerializer, RelationshipSerializer, MeetingSerializer, PreferencesSerializer, MyInvitationSerializer, InvitationSerializer 

# local permission
from rest.permissions import IsUser, IsMentorMenteeORSuper

# To choose actions for viewset
from rest_framework import viewsets, mixins

class SeekingRelationshipViewSet(mixins.RetrieveModelMixin, 
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    End point to list those members who are seeking either mentor or mentee
    """
    
    serializer_class = SeekingSerializer #change this (somehow) to user!
    
    #attempt to filter by seeking type:
    def get_queryset(self):
      queryset = Preferences.objects.all()
      mentor = self.request.query_params.get('mentor', None)
      mentee = self.request.query_params.get('mentee', None)
      """  
      if mentor then is_seeking_mentor set to true
      """
      if mentor is not None:
          queryset = queryset.filter(is_seeking_mentor=True)
      """
      if mentee then is_seeking_mentee set to true
      """
      if mentee is not None:
          queryset = queryset.filter(is_seeking_mentee=True)

      return queryset


class UserViewSet(
#		   mixins.CreateModelMixin, 
                   mixins.RetrieveModelMixin, 
                   mixins.UpdateModelMixin,
#                  mixins.DestroyModelMixin, 
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    # only allow user to see this view TODO extend to IsUserOrManager
    permission_classes = (IsUser,)

    #queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    #Attempt to filter the results set
    def get_queryset(self):
      """
      if is_superuser field set then filter by this
      """
      queryset = User.objects.all().order_by('-date_joined')
# To be used when we admin accounts etc
#      issuper = self.request.query_params.get('is_superuser', None)
#      if issuper is not None:
#          queryset = queryset.filter(is_superuser=issuper)
#      username = self.request.query_params.get('username',None)
#      if username is not None:
#          queryset = queryset.filter(username=username)
      return queryset

#class ProxyViewSet(viewsets.ModelViewSet):
#    """
#    API endpoint that provides retrieval of user by an authorized proxy.
#    """
#    serializer_class = UserSerializer
#
#    #Attempt to filter the results set
#    def get_queryset(self):
#      """
#      if is_superuser field set then filter by this
#      """
#      queryset = User.objects.all().order_by('-date_joined')
#      username = self.request.query_params.get('username',None)
#      if username is not None:
#          queryset = queryset.filter(username=username)
#      return queryset


class MyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    #queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    #Attempt to filter the results set
    def get_queryset(self):
      """
      if is_superuser field set then filter by this
      """
      queryset = User.objects.all().order_by('-date_joined')
      queryset = queryset.filter(username=self.request.user)
      #issuper = self.request.query_params.get('is_superuser', None)
      #if issuper is not None:
      #    queryset = queryset.filter(is_superuser=issuper)
      #username = self.request.query_params.get('username',None)
      #if username is not None:
      #    queryset = queryset.filter(username=self.request.username)
      return queryset

#    # I think this is handled by ModelViewSet and serialzer save on request.data
#    #MyViewSet contains a primary key so that PUT requests are setup
#    def update():
#      """
#      Provide update of core user details (email, mentorship_preferences)
#      However other Views will take care of associated entities eg invitations, relationships
#      """
      

class MyPreferencesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    #queryset = User.objects.all().order_by('-date_joined')
    serializer_class = PreferencesSerializer

    #Attempt to filter the results set
    def get_queryset(self):
      """
      if is_superuser field set then filter by this
      """
      queryset = Preferences.objects.all()
      queryset = queryset.filter(user_id=self.request.user)
      #issuper = self.request.query_params.get('is_superuser', None)
      #if issuper is not None:
      #    queryset = queryset.filter(is_superuser=issuper)
      #username = self.request.query_params.get('username',None)
      #if username is not None:
      #    queryset = queryset.filter(username=self.request.username)
      return queryset


class MenteeViewSet(mixins.RetrieveModelMixin, 
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    """
    View the relationship where the current user is the Mentor
    """
    serializer_class = RelationshipSerializer

    def get_queryset(self):
      """
      Filter the realtionships
      """
      queryset = Relationship.objects.all()
      queryset = queryset.filter(mentor=self.request.user,is_active=True)
      return queryset


class MentorViewSet(mixins.RetrieveModelMixin, 
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    """
    View the relationship where the current user is the Mentor
    """
    serializer_class = RelationshipSerializer

    def get_queryset(self):
      """
      Filter the realtionships
      """
      queryset = Relationship.objects.all()
      queryset = queryset.filter(mentee=self.request.user,is_active=True)
      return queryset

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

#class BasicRelationshipViewSet(viewsets.ModelViewSet):
class BasicRelationshipViewSet(mixins.CreateModelMixin, 
                   mixins.RetrieveModelMixin, 
                   mixins.UpdateModelMixin,
#                   mixins.DestroyModelMixin, do not allow destroy
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    """
    API endpoint that allows relationships to be viewed or edited.
    """
    permission_classes = (IsMentorMenteeORSuper,)
    queryset = Relationship.objects.all()
    serializer_class = BasicRelationshipSerializer



class RelationshipViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Relationship.objects.all()
    serializer_class = RelationshipSerializer


class MeetingViewSet(mixins.CreateModelMixin, 
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    API endpoint that allows Meetings to be viewed or edited.
    """
    # There is no object on post so a specific has permission needs to 
    # check the incoming form to check that user is one of mentor/mentee
    # or we can do that in here (more obvious)

#   This works at object level and when posting we are not operating on an object
#    permission_classes = (IsMentorMenteeORSuper,)
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer


class PreferencesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Preferences to be viewed or edited.
    """
    queryset = Preferences.objects.all()
    serializer_class = PreferencesSerializer

 
class InvitationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Invitations to be viewed or edited.
    """
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer

#    This will be received by the Serializer after seriazer.is_valid check - therefore can not use
#    def perform_create(self, serializer):
#        serializer.save(created_by=self.request.user)

class MyInvitationViewSet(mixins.ListModelMixin,
                   	viewsets.GenericViewSet):
    """
    API endpoint to list the invitations that the current user has been included in
    The view will split this list into sender / recipient, mentee / mentor
    """
    # For simplicity we want to return the mentor and mentee as we end up displaying these in lists (and can avoid a further request)
    serializer_class = MyInvitationSerializer

    #Attempt to filter the results set
    def get_queryset(self):
      """
      if is_superuser field set then filter by this
      """
      queryset = Invitation.objects.all().order_by('-created_on')
      queryset = queryset.filter(deactivated_on__isnull=True).filter( Q(created_by=self.request.user) | Q(mentee=self.request.user) | Q(mentor=self.request.user))

      return queryset

#class ProfileViewSet(viewsets.ModelViewSet):
#    """
#    API endpoint that allows Invitations to be viewed or edited.
#    """
#    queryset = Profile.objects.all()
#    serializer_class = ProfileSerializer

  

