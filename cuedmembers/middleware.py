"""
Middleware for CUED Members application

"""
from .models import Member

class MemberMiddleware:
    """Middleware which looks up a Member corresponding to the current
    logged in user and makes it available via the request.cued_member
    attribute.

    If the current user is not logged in or is not a CUED member then
    request.cued_member is None.

    """
    def process_request(self, request):
        # pylint:disable=no-self-use
        user = getattr(request, 'user', None)
        if user is None or not user.is_authenticated():
            request.cued_member = None
            return

        try:
            request.cued_member = Member.objects.get(user=user)
        except Member.DoesNotExist:
            request.cued_member = None
