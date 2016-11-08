from django.shortcuts import render

# Create your views here.


from django.contrib.auth.models import User, Group
from mentoring.models import Relationship, Meeting
from matching.models import Preferences, Invitation
from rest.models import Profile

from rest_framework import viewsets
from django.views.decorators.csrf import ensure_csrf_cookie
#from edpcmentoring.rest.serializers import UserSerializer, GroupSerializer
from serializers import UserSerializer, GroupSerializer, RelationshipSerializer, MeetingSerializer, PreferencesSerializer, InvitationSerializer #, ProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
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
      issuper = self.request.query_params.get('is_superuser', None)
      if issuper is not None:
          queryset = queryset.filter(is_superuser=issuper)
      username = self.request.query_params.get('username',None)
      if username is not None:
          queryset = queryset.filter(username=username)
      return queryset

class ProxyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that provides retrieval of user by an authorized proxy.
    """
    serializer_class = UserSerializer

    #Attempt to filter the results set
    def get_queryset(self):
      """
      if is_superuser field set then filter by this
      """
      queryset = User.objects.all().order_by('-date_joined')
      username = self.request.query_params.get('username',None)
      if username is not None:
          queryset = queryset.filter(username=username)
      return queryset


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


class MenteeViewSet(viewsets.ModelViewSet):
    """
    View the relationship where the current user is the Mentor
    """
    serializer_class = RelationshipSerializer

    def get_queryset(self):
      """
      Filter the realtionships
      """
      queryset = Relationship.objects.all()
      queryset = queryset.filter(mentor=self.request.user)
      return queryset


class MentorViewSet(viewsets.ModelViewSet):
    """
    View the relationship where the current user is the Mentor
    """
    serializer_class = RelationshipSerializer

    def get_queryset(self):
      """
      Filter the realtionships
      """
      queryset = Relationship.objects.all()
      queryset = queryset.filter(mentee=self.request.user)
      return queryset

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class RelationshipViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Relationship.objects.all()
    serializer_class = RelationshipSerializer


class MeetingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Meetings to be viewed or edited.
    """
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


#class ProfileViewSet(viewsets.ModelViewSet):
#    """
#    API endpoint that allows Invitations to be viewed or edited.
#    """
#    queryset = Profile.objects.all()
#    serializer_class = ProfileSerializer

  

