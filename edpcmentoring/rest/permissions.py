from rest_framework import permissions

class IsUser(permissions.BasePermission):
	'''
	Custome permission access if current users is the user
	'''

	def has_object_permission(sel, request, view, obj):

		return obj == request.user




class IsMentorMenteeORSuper(permissions.BasePermission):
	'''
	Cunstom permission access is user one of above

        TODO modify superuser to a particular role
	'''

	def has_object_permission(sel, request, view, obj):
		print obj.mentee
		print obj.mentor
		print request.user
		print request.user.is_superuser		
		return obj.mentee == request.user or obj.mentor == request.user or request.user.is_superuser
