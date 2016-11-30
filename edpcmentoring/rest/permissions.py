from rest_framework import permissions

class IsUser(permissions.BasePermission):
	'''
	Custom permission access if current users is the user
	'''

	def has_object_permission(sel, request, view, obj):

		return obj == request.user




class IsMentorMenteeORSuper(permissions.BasePermission):
	'''
	Custom permission access is user one of above

        TODO modify superuser to a particular role
	'''

	def has_object_permission(sel, request, view, obj):
		return obj.mentee == request.user or obj.mentor == request.user or request.user.is_superuser
