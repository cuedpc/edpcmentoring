from django.contrib.auth.models import User, Group
from mentoring.models import Relationship, Meeting
from matching.models import Preferences, Invitation 
from cuedmembers.models import Member, ResearchGroup, Division 

from django.core.exceptions import ValidationError, PermissionDenied

from rest_framework import serializers

#include the nested relationships: http://www.django-rest-framework.org/api-guide/relations/#nested-relationships

class PreferencesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Preferences
        fields = ('is_seeking_mentor','is_seeking_mentee','mentor_requirements','mentee_requirements')

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

 
class SeekingSerializer(serializers.HyperlinkedModelSerializer):
    '''
    A user seeking either mentor or mentee
    '''
    user = MentorSerializer(many=False, read_only=True); # Fixme should be Mentor OR Mentee new object required?
    class Meta:
        model = Preferences
        fields = ('is_seeking_mentor','is_seeking_mentee','mentor_requirements','mentee_requirements','user')

 
#TODO remove this:?  
class RawRelationshipSerializer(serializers.HyperlinkedModelSerializer):
    mentor = MentorSerializer(many=False)
    mentee = MenteeSerializer(many=False)
    class Meta:
        model = Relationship
        fields = ('mentor', 'mentee', 'started_on', 'ended_on', 'ended_by', 'is_active','meetings')

class BasicRelationshipSerializer(serializers.HyperlinkedModelSerializer):
    #mentor = MentorSerializer(many=False)
    #mentee = MenteeSerializer(many=False)
    class Meta:
        model = Relationship
 
        fields = ('id', 'started_on', 'ended_on', 'ended_by', 'is_active')

    def update(self, instance, validated_data):
        '''
        If we are ending this relation we need to call the model method    
        '''
        if (instance.ended_on is None and validated_data.get('is_active') == False) :    
            instance.end(self.context['request'].user)
            instance.save()

        #Note we have prevented any other modification, but is_active to false! 
        return instance
 
class MeetingSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Meeting
        fields =('id','relationship', 'held_on', 'approximate_duration')

    # TODO given a meeting and the current user
    # Find whether the current user is one of the mentor or mentee in the relationship
    # options:
    #     a, Create a meeting object and test from it whether this is the case?
    #      b, retrieve the relatioship and check that the current user is either mentor / mentee


    def create(self, validated_data):
        # TODO check whether a mentee or mentor is provided (perhaps both) - where are django policies?
        # WE could put this in a permission policy but perhaps more obvious here
        # Only allow create if request.user is mentee or mentor
       
        # get the current authenticated user 
        user = self.context['request'].user

        # create a meeting if (is mentor || mentee || is_superuser )
        # NB if we passed the relationship object we should be able to identify this straight away!

        # TODO Move this criteria soemwhere else
        rel = validated_data['relationship']    
        if rel.mentee.id == user.id or rel.mentor.id == user.id or user.is_superuser:
           return Meeting.objects.create(**validated_data) # - tests againt useryy
        
        # or return our error
        raise serializers.ValidationError("Error creating meeting - invalid user!")

class RelationshipSerializer(serializers.HyperlinkedModelSerializer):
    meetings = MeetingSerializer(many=True)
    mentor = MentorSerializer(many=False)
    mentee = MenteeSerializer(many=False)
    class Meta:
        model = Relationship
        fields = ('id','mentor', 'mentee', 'started_on', 'ended_on', 'ended_by', 'is_active','meetings')

# We are Not provding PUT or POST to RelationshipViewSet
#    def update(self, instance, validated_data):
#        '''
#        If we are ending this relation we need to call the model method    
#        '''
#        if (instance.ended_on is None and validated_data.get('is_active') == False) :    
#            instance.end(self.context['request'].user)
#            instance.save()
#
#        '''
#        atm prevent from occuring -only status change allowed
#        else:
#        instance.mentor=validated_data.get('mentor',instance.mentor)
#        instance.mentee=validated_data.get('mentee',instance.mentee)
#        instance.started_on=validated_data.get('started_on',instance.started_on)
#        instance.is_active=validated_data.get('is_active',instance.is_active)
#        instance.meetings=validated_data.get('meetings',instance.meetings)
#        '''
#        return instance


class InvitationSerializer(serializers.HyperlinkedModelSerializer):

    created_by = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='user-detail', required=False, default=serializers.CurrentUserDefault())
    mentee = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='user-detail', required=False,  default=serializers.CurrentUserDefault())
    mentor = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='user-detail', required=False,  default=serializers.CurrentUserDefault() )
    class Meta:
        model = Invitation
        fields =('id','mentor','mentee','created_by','created_on','mentor_response','mentee_response','deactivated_on','created_relationship')
    #FIXME: add two validators:
    #1, Mentee != Mentor
    #2, user is admin or user = mentee or user =mentor 
    validators = []

    def update(self, instance, validated_data):
        '''
        Prevent mentor,mentee,created_by to be modified on update
        '''
        user = self.context['request'].user

        if (  user.is_superuser or
        (( validated_data.get('mentor_response') == 'A' or  validated_data.get('mentor_response') == 'D' ) and user == instance.mentor) or
        (( validated_data.get('mentee_response') == 'A' or  validated_data.get('mentee_response') == 'D' ) and user == instance.mentee) ):

            if (    validated_data.get('mentor_response') == 'A' or  validated_data.get('mentee_response') == 'A'  ):
                instance.respond(user, True) 
            if (  validated_data.get('mentor_response') == 'D' or   validated_data.get('mentee_response') == 'D'  ):
                instance.respond(user, False)

        #instance.mentor_response = validated_data.get('mentor_response',instance.mentor_response)
        #instance.mentee_response = validated_data.get('mentee_response',instance.mentee_response)
        #TODO if the response deactivates the invitaton this is to be done in the model 
        #instance.deactivated_on = validated_data.get('deactivated_on',instance.deactivated_on)
        #TODO if the response produces a relationship this is to be triggered in the model
        #instance.created_relationship = validated_data.get('mentee_response',instance.created_relationship)

            instance.save()
            return instance

    # or return our error
        raise serializers.ValidationError("Error creating meeting - invalid user!")
        #return 
    
    def create(self, validated_data):
        user= validated_data['created_by']
        mentee=validated_data.get('mentee',user)
        mentor=validated_data.get('mentor',user)
        invitation = Invitation(mentor=mentor,mentee=mentee,created_by=user)
        try:
            invitation.clean()
            invitation.both_willing()
            invitation.save()
            return invitation 
        except ValidationError as e:
            raise serializers.ValidationError("Error creating invitation: "+str(e))
            #return


class MyInvitationSerializer(serializers.HyperlinkedModelSerializer):
  
    created_by = MentorSerializer(many=False, read_only=True, required=False); # Fixme 
    mentee = MentorSerializer(many=False, read_only=True, required=False); # Fixme 
    mentor = MentorSerializer(many=False, read_only=True, required=False); # Fixme 
    class Meta:
        model = Invitation
        fields =('id','mentor','mentee','created_by','created_on','mentor_response','mentee_response','deactivated_on','created_relationship')






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


