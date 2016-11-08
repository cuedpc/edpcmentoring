from django.contrib.auth.models import User, Group
from mentoring.models import Relationship, Meeting
from matching.models import Preferences, Invitation 
from cuedmembers.models import Member, ResearchGroup, Division 

from rest_framework import serializers

#include the nested relationships: http://www.django-rest-framework.org/api-guide/relations/#nested-relationships

class PreferencesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Preferences
        fields = ('is_seeking_mentor','is_seeking_mentee','mentor_requirements','mentee_requirements')

class InvitationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Invitation
        fields =('mentor','mentee','created_by','created_on','mentor_response','mentee_response','deactivated_on','created_relationship')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class DivisionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Division
        fields =('name','letter')

class ResearchGroupSerializer(serializers.HyperlinkedModelSerializer):
    division = DivisionSerializer(many=False, read_only=False)
    class Meta:
        model = ResearchGroup
        fields =('name','division')

class MemberSerializer(serializers.HyperlinkedModelSerializer):
    research_group = ResearchGroupSerializer(many=False, read_only=False)
    class Meta:
        model = Member
        fields =('first_names','research_group')



class MenteeSerializer(serializers.HyperlinkedModelSerializer):
    '''
       A special type of user who is a Mentor
    '''
    cued_member = MemberSerializer(many=False, read_only=True) 

    class Meta:
        model = User
        fields = ('id','is_superuser','url', 'username', 'email', 'first_name', 'last_name', 'cued_member' )

 
class MentorSerializer(serializers.HyperlinkedModelSerializer):
    '''
       A special type of user who is a Mentor
    '''
    cued_member = MemberSerializer(many=False, read_only=True) 

    class Meta:
        model = User
        fields = ('id','is_superuser','url', 'username', 'email', 'first_name', 'last_name', 'cued_member' )

  
  
class RawRelationshipSerializer(serializers.HyperlinkedModelSerializer):
    mentor = MentorSerializer(many=False)
    mentee = MenteeSerializer(many=False)
    class Meta:
        model = Relationship
        fields = ('mentor', 'mentee', 'started_on', 'ended_on', 'ended_by', 'is_active','meetings')


class MeetingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Meeting
        fields =('relationship', 'held_on', 'approximate_duration')


class RelationshipSerializer(serializers.HyperlinkedModelSerializer):
    meetings = MeetingSerializer(many=True)
    mentor = MentorSerializer(many=False)
    mentee = MenteeSerializer(many=False)
    class Meta:
        model = Relationship
        fields = ('id','mentor', 'mentee', 'started_on', 'ended_on', 'ended_by', 'is_active','meetings')

class UserSerializer(serializers.HyperlinkedModelSerializer):

    mentorship_preferences = PreferencesSerializer(many=False, read_only=False)
    #mentorship_preferences = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    mentee_invitations = InvitationSerializer(many=True, read_only=True)
    mentor_invitations = InvitationSerializer(many=True, read_only=True)
    mentee_relationships = RelationshipSerializer(many=True, read_only=True)
    mentor_relationships = RelationshipSerializer(many=True, read_only=True)
    cued_member = MemberSerializer(many=False, read_only=True) 

    class Meta:
        model = User
        fields = ('id','is_superuser','url', 'username', 'first_name', 'last_name', 'email', 'cued_member', 'groups','mentorship_preferences','mentee_invitations','mentor_invitations','mentee_relationships','mentor_relationships')

    def create(self, validated_data):
        # TODO check whether validated_data includes 'mentorship_preferences','mentee_invitations','mentor_invitations','mentee_relationships','mentor_relationships'
        # As these need to be added as assoictions
        user = User.objects.create(**validated_data)
        return user 


    def update(self, instance, validated_data):
        """
        Allow the user to update preferences - only atm
        """
	prefs = instance.mentorship_preferences
        prefs_new = validated_data.pop('mentorship_preferences')
 
	instance.email=validated_data.get('email',instance.email)
        instance.save()

        prefs.is_seeking_mentor = prefs_new.get('is_seeking_mentor',prefs.is_seeking_mentor)
        prefs.is_seeking_mentee = prefs_new.get('is_seeking_mentee',prefs.is_seeking_mentee)
        prefs.mentor_requirements = prefs_new.get('mentor_requirements',prefs.mentor_requirements)
        prefs.mentee_requirements = prefs_new.get('mentee_requirements',prefs.mentee_requirements)
        prefs.save()

        return instance;


