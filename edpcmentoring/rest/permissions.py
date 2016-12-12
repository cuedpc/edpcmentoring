from rest_framework import permissions
from rolepermissions.verifications import has_permission

class IsUser(permissions.BasePermission):
    '''
    Custom permission access if current users is the user
    '''
    def has_object_permission(sel, request, view, obj):
        return obj == request.user

class IsMatchMaker(permissions.BasePermission):
    '''
    This user has been assigned the matchmaker role
    '''
    def has_permission(self,request,view):
#        return has_permission(request.user,'make_matches')  
        return request.user.has_perm('matching.matchmake')


class IsMentorMenteeORSuper(permissions.BasePermission):
    '''
    Custom permission access is user one of above

    TODO modify superuser to a particular role
    '''

    def has_object_permission(sel, request, view, obj):
        return obj.mentee == request.user or obj.mentor == request.user or request.user.is_superuser
