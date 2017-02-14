from django.contrib.auth.models import User, Group
from mentoring.models import Relationship, Meeting
from matching.models import Preferences, Invitation 
from cuedmembers.models import Member, ResearchGroup, Division 

from django.core.exceptions import ValidationError, PermissionDenied

from rest_framework import serializers

# To allow the creation of an object whose related objects already exist:
# http://www.erol.si/2015/09/django-rest-framework-nestedserializer-with-relation-and-crud/
from rest_framework.fields import empty
 
class RelationModelSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=empty, **kwargs):
        self.is_relation = kwargs.pop('is_relation', False)
        super(RelationModelSerializer, self).__init__(instance, data, **kwargs)

    def validate_empty_values(self, data):
        if self.is_relation:
            model = getattr(self.Meta, 'model')
            model_pk = model._meta.pk.name

            if not isinstance(data, dict):
                error_message = self.default_error_messages['invalid'].format(datatype=type(data).__name__)
                raise serializers.ValidationError(error_message)

            if not model_pk in data:
                raise serializers.ValidationError({model_pk: model_pk + ' is required'})

            try:
                instance = model.objects.get(pk=data[model_pk])
                return True, instance
            except:
                raise serializers.ValidationError({model_pk: model_pk + ' is not valid'})

        return super(RelationModelSerializer, self).validate_empty_values(data)




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

# TODO consolidate Mentee and Mentor Serializer into depth=1 User serializer

class MenteeSerializer(RelationModelSerializer):
    '''
       A special type of user who is a Mentor
    '''
    cued_member = MemberSerializer(many=False, read_only=True) 

    class Meta:
        model = User
        fields = ('id','is_superuser','url', 'username', 'email', 'first_name', 'last_name', 'cued_member' )

 
class MentorSerializer(RelationModelSerializer):
    '''
       A special type of user who is a Mentor
    '''
    cued_member = MemberSerializer(many=False, read_only=True) 

    class Meta:
        model = User
        fields = ('id','is_superuser','url', 'username', 'email', 'first_name', 'last_name', 'cued_member' )

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

#http://stackoverflow.com/questions/28163556/how-do-you-filter-a-nested-serializer-in-django-rest-framework
class ActiveRelationshipListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(ended_on__isnull=True)
        return super(ActiveRelationshipListSerializer, self).to_representation(data)

class ActiveRelationshipSerializer(serializers.HyperlinkedModelSerializer):
    meetings = MeetingSerializer(many=True)
    mentor = MentorSerializer(many=False)
    mentee = MenteeSerializer(many=False)
    class Meta:
        list_serializer_class = ActiveRelationshipListSerializer
        model = Relationship
        fields = ('id','mentor', 'mentee', 'started_on', 'ended_on', 'ended_by', 'is_active','meetings')


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

#http://stackoverflow.com/questions/28163556/how-do-you-filter-a-nested-serializer-in-django-rest-framework
class ActiveInvitationListSerializer(serializers.ListSerializer):
 
    def to_representation(self, data):
        data = data.filter(deactivated_on__isnull=True)
        return super(ActiveInvitationListSerializer, self).to_representation(data)

## TODO inherit and override the InvitationSerializer class rathe than define a new one (can we?)
#
#class ActiveInvitationSerializer(serializers.HyperlinkedModelSerializer):
#    created_by = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='user-detail', required=False, default=serializers.CurrentUserDefault())
#
#    mentee = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='user-detail', required=False,  default=serializers.CurrentUserDefault())
#    mentor = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='user-detail', required=False,  default=serializers.CurrentUserDefault() )
# 
#    class Meta:
#        list_serializer_class = ActiveInvitationListSerializer
#        model = Invitation
#        fields =('id','mentor','mentee','created_by','created_on','mentor_response','mentee_response','deactivated_on','created_relationship')


class InvitationSerializer(serializers.ModelSerializer):
	
    # created_by - used to circumvent the is_valid test (it will be overwritten with the request user during create)
    # created_by = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='user-detail', required=False, default=serializers.CurrentUserDefault())
    created_by = MenteeSerializer(many=False, is_relation=True, default=serializers.CurrentUserDefault() )

    #mentee = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='user-detail', required=False,  default=serializers.CurrentUserDefault())
    mentee = MenteeSerializer(many=False, read_only=False, is_relation=True, default=serializers.CurrentUserDefault())
    #mentor = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='user-detail', required=False,  default=serializers.CurrentUserDefault() )
    mentor = MentorSerializer(many=False, read_only=False, is_relation=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = Invitation
        fields =('id','mentor','mentee','created_by','created_on','mentor_response','mentee_response','deactivated_on','created_relationship')
    #FIXME: add two validators:
    #1, Mentee != Mentor
    #2, user is admin or user = mentee or user =mentor 
    validators = []

    def update(self, instance, validated_data):
        '''
        Some validation specific to inivaation update (acceptance or decline)
        Prevent mentor,mentee,created_by to be modified on update - only a valid response will be applied
        '''
        user = self.context['request'].user

        if (  user.has_perm('matchmake') or
        (( validated_data.get('mentor_response') == 'A' or  validated_data.get('mentor_response') == 'D' ) and user == instance.mentor) or
        (( validated_data.get('mentee_response') == 'A' or  validated_data.get('mentee_response') == 'D' ) and user == instance.mentee) ):

            if (    validated_data.get('mentor_response') == 'A' or  validated_data.get('mentee_response') == 'A'  ):
                instance.respond(user, True) 
            if (  validated_data.get('mentor_response') == 'D' or   validated_data.get('mentee_response') == 'D'  ):
                instance.respond(user, False)
#            if (user.has_perm('matchmake')): #done in model if matchmake?
#                instance.created_by = user

            instance.save()
            return instance

        # or return our error
        raise serializers.ValidationError("Error creating meeting - invalid user!")
    
#    def validate_mentee(self,value):
#        raise serializers.ValidationError("problem with the mentee: "+str(mentee))

    def create(self, validated_data):
#        user= validated_data['created_by'] ignore user passed by client (can we trust that )
        user = self.context['request'].user
# TODO what validates the data and how do we pass a valid mentor  / mentee
#        mentee=validated_data.get('mentee',user)
        mentee=validated_data.get('mentee')
#        mentor=validated_data.get('mentor',user)
        mentor=validated_data.get('mentor')
        invitation = Invitation(mentor=mentor,mentee=mentee,created_by=user,mentee_response=validated_data.get('mentee_response'),mentor_response=validated_data.get('mentor_response'))
        try:
            invitation.clean()
            invitation.both_willing()
            invitation.save()
            return invitation 
        except ValidationError as e:
            raise serializers.ValidationError("Error creating invitation: "+str(e))
            #return


class ActiveInvitationSerializer(InvitationSerializer):
#    created_by = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='user-detail', required=False, default=serializers.CurrentUserDefault())
#
#    mentee = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='user-detail', required=False,  default=serializers.CurrentUserDefault())
#    mentor = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='user-detail', required=False,  default=serializers.CurrentUserDefault() )
# 
    class Meta:
        list_serializer_class = ActiveInvitationListSerializer
        model = Invitation
        fields =('id','mentor','mentee','created_by','created_on','mentor_response','mentee_response','deactivated_on','created_relationship')




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
    mentee_invitations = ActiveInvitationSerializer(many=True, read_only=True)
    mentor_invitations = ActiveInvitationSerializer(many=True, read_only=True)
    mentee_relationships = ActiveRelationshipSerializer(many=True, read_only=True)
    mentor_relationships = ActiveRelationshipSerializer(many=True, read_only=True)
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

 
class MatchSeekingSerializer(serializers.HyperlinkedModelSerializer):
    '''
    A user seeking either mentor or mentee
    '''
    user = UserSerializer(many=False, read_only=True); # Fixme should be Mentor OR Mentee new object required?
    class Meta:
        model = Preferences
        fields = ('is_seeking_mentor','is_seeking_mentee','mentor_requirements','mentee_requirements','user')
        depth = 2
 

