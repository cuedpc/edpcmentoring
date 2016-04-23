"""
Middleware for the mentoring application.

"""
from .models import StaffMember

class StaffMemberMiddleware:
    """Middleware which looks up a StaffMember corresponding to the current
    logged in user and makes it available via the request.staff_member
    attribute.

    """
    def process_request(self, request):
        # pylint:disable=no-self-use,no-member

        user = getattr(request, 'user', None)
        if user is None or not user.is_authenticated():
            request.staff_member = None
            return

        try:
            request.staff_member = StaffMember.objects.get(user=user)
        except StaffMember.DoesNotExist:
            request.staff_member = None
