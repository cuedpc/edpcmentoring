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

#class InvitationSerializer(serializers.HyperlinkedModelSerializer):
#
#    user = MentorSerializer(many=False, read_only=True, required=False); # Fixme 
#    mentee = MentorSerializer(many=False, read_only=True, required=False); # Fixme 
#    mentor = MentorSerializer(many=False, read_only=True, required=False); # Fixme 
#
#    class Meta:
#        model = Invitation
#        fields =('mentor','mentee','created_by','created_on','mentor_response','mentee_response','deactivated_on','created_relationship')
#
#    def create(self, validated_data):
#        # TODO check whether a mentee or mentor is provided (perhaps both) - where are django policies?
#	# Only allow creation of invitation if current user any of the following:
#	# Mentor, Mentee or has admin writes
#        # Also only allow creation if both parties are searching!?
#        # As these need to be added as associations
#       
#        # get the current authenticated user 
#        user = self.context['request'].user
#
#        invitation = Invitataions.objects.create({mentor:user,mentee:user,create_by:user})
#        #invitation = Invitataions.objects.create(**validated_data)
#        return invitation 


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


#class PKUserSerializer(serializers.HyperlinkedModelSerializer):
#    '''
#	Serialize all the associated fields with primary key serializers
#    '''
#
#    mentorship_preferences = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
#    mentee_invitations = serializers.PrimaryKeyRelatedField(many=True, read_only=True) 
#    mentor_invitations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#    mentee_relationships =  serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#    mentor_relationships = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#    cued_member = serializers.PrimaryKeyRelatedField(many=False, read_only=True) 
#
#    class Meta:
#        model = User
#        fields = ('id','is_superuser','url', 'username', 'first_name', 'last_name', 'email', 'cued_member', 'groups','mentorship_preferences','mentee_invitations','mentor_invitations','mentee_relationships','mentor_relationships')
#


class MeetingSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Meeting
        fields =('relationship', 'held_on', 'approximate_duration')

    # TODO given a meeting and the current user
    # Find whether the current user is one of the mentor or mentee in the relationship
    # options:
    #     a, Create a meeting object and test from it whether this is the case?
    #	  b, retrieve the relatioship and check that the current user is either mentor / mentee


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
	return 
	
 

class RelationshipSerializer(serializers.HyperlinkedModelSerializer):
    meetings = MeetingSerializer(many=True)
    mentor = MentorSerializer(many=False)
    mentee = MenteeSerializer(many=False)
    class Meta:
        model = Relationship
        fields = ('id','mentor', 'mentee', 'started_on', 'ended_on', 'ended_by', 'is_active','meetings')

    def update(self, instance, validated_data):
	'''
        If we are ending this relation we need to call the model method	
	'''
	if (instance.ended_on is None and validated_data.get('is_active') == False) :	
	   instance.end(self.context['request'].user)
	   instance.save()

	'''
atm prevent from occuring -only status change allowed
        else:
	   instance.mentor=validated_data.get('mentor',instance.mentor)
	   instance.mentee=validated_data.get('mentee',instance.mentee)
	   instance.started_on=validated_data.get('started_on',instance.started_on)
           instance.is_active=validated_data.get('is_active',instance.is_active)
	   instance.meetings=validated_data.get('meetings',instance.meetings)
	'''
        return instance


class InvitationSerializer(serializers.HyperlinkedModelSerializer):

#    created_by = MentorSerializer(many=False, read_only=True, required=False); # Fixme 
#    mentee = MentorSerializer(many=False, read_only=True, required=False); # Fixme 
#    mentor = MentorSerializer(many=False, read_only=True, required=False); # Fixme 
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


	# TODO Move this validation soemwhere else - allow update it mentor/mentee is responding or is_superuser
        # we are acting on an object so could use permissions.py and add a permission to view
	#rel = validated_data['relationship']	
	#rel = instance.relationship
	mentor_response=validated_data.get('mentor_response')
	mentee_response=validated_data.get('mentee_response')

#	if (  user.is_superuser or
#	    (( mentor_response == 'A' or  mentor_response == 'D' ) and user == instance.mentor) or
#	    (( mentee_response == 'A' or  mentee_response == 'D' ) and user == instance.mentee) ):

#	if 1==1:		
#        	if (    mentor_response == 'A' or  mentee_response == 'A'  ):
#			instance.respond(user, True) 
#        	if (    mentor_response == 'D' or  mentee_response == 'D'  ):
#			instance.respond(user, False)


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
	return 
	

    def create(self, validated_data):
        # TODO check whether a mentee or mentor is provided (perhaps both) - where are django policies?
	# Only allow creation of invitation if current user any of the following:
	# Mentor, Mentee or has admin writes
        # Also only allow creation if both parties are searching!?
        # As these need to be added as associations
       
        # get the current authenticated user 
        # user = self.context['request'].user
        user= validated_data['created_by']
	mentee=validated_data.get('mentee',user)
	mentor=validated_data.get('mentor',user)

        #FIXME move these into a validator
        #TODO test either mentee or mentor == user!! 
        #     and mentee != mentor
	#IF not return error - or access denied!
	if mentee == mentor:
		raise serializers.ValidationError("Error creating invitation - invitation not created")
		return 
        #TODO also check for user 'add_invitation' permission
	if user != mentee and  user != mentor :
		raise serializers.ValidationError("Error creating invitation - user neither mentee or mentor")
		return 
	#TODO fix me (needs puttin (elsewhere):
	#auto accept the calling side
	mentor_response=''
	mentee_response=''
	if user == mentee:
		mentee_response='A'
	if user == mentor:
		mentor_response='A'

	invitation = Invitation(mentor=mentor,mentee=mentee,created_by=user,mentor_response=mentor_response,mentee_response=mentee_response)
	invitation.save()
        #invitation = Invitation.objects.create({'mentor':user,'mentee':user,'created_by':user})
        #invitation = Invitation.objects.create(**validated_data)
        return invitation 


class MyInvitationSerializer(serializers.HyperlinkedModelSerializer):

#   TODO - prevent POST PUT on this class for view only?!
    created_by = MentorSerializer(many=False, read_only=True, required=False); # Fixme 
    mentee = MentorSerializer(many=False, read_only=True, required=False); # Fixme 
    mentor = MentorSerializer(many=False, read_only=True, required=False); # Fixme 
#    created_by = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='user-detail', required=False, default=serializers.CurrentUserDefault())
#    mentee = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='user-detail', required=False,  default=serializers.CurrentUserDefault())
#    mentor = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='user-detail', required=False,  default=serializers.CurrentUserDefault() )
    class Meta:
        model = Invitation
        fields =('id','mentor','mentee','created_by','created_on','mentor_response','mentee_response','deactivated_on','created_relationship')
	#FIXME: add two validators:
	#1, Mentee != Mentor
	#2, user is admin or user = mentee or user =mentor 
	validators = []

    def create(self, validated_data):
	#FIME Do not allow
	return




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


