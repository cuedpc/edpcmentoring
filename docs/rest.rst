REST Application
===============

This application handles access to the database through 'RESTful' methods utilizing the rest_framework package

Authorization
-------------

Access to endpoints is managed either by the use of a permissions_classses array in the view file::

  permissions_classes = (IsMatchMaker, )
  
Which would use the user defined rest_framework.permissions class (for example found in permissions.py)::
  
  class IsMatchMaker(permissions.BasePermission):
      '''
     This user has been assigned the matchmaker role
     '''
      def has_permission(self,request,view):
          return request.user.has_perm('matching.matchmake')

**Or** specific tests in the serializer methods eg  InvitationSerializer.update::

    def update(self, instance, validated_data):
        '''
        Some validation specific to inivaation update (acceptance or decline)
        Prevent mentor,mentee,created_by to be modified on update - only a valid response will be applied
        '''
        user = self.context['request'].user

        if (  user.is_superuser or
        (( validated_data.get('mentor_response') == 'A' or  validated_data.get('mentor_response') == 'D' ) and user == instance.mentor) or
        (( validated_data.get('mentee_response') == 'A' or  validated_data.get('mentee_response') == 'D' ) and user == instance.mentee) ):

            if (    validated_data.get('mentor_response') == 'A' or  validated_data.get('mentee_response') == 'A'  ):
                instance.respond(user, True)
            if (  validated_data.get('mentor_response') == 'D' or   validated_data.get('mentee_response') == 'D'  ):
                instance.respond(user, False)
            instance.save()
            return instance

        # or return our error
        raise serializers.ValidationError("Error creating meeting - invalid user!")


