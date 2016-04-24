from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def member_required(f):
    """A decorator which wraps login_required additionally checking that the
    logged in user is an active member of CUED.

    If the user is logged in but not a member of CUED, or is an inactive member,
    a PermissionDenied exception is raised.

    This deocrator requires that the cuedmembers.CuedMemberMiddleware be active.

    """
    # Wrap function with login_required
    f = login_required(f)

    @wraps(f)
    def wrapper(request, *args, **kwargs):
        user = getattr(request, 'user')
        cued_member = getattr(request, 'cued_member')
        if user is not None and user.is_authenticated():
            if cued_member is None or not cued_member.is_active:
                raise PermissionDenied()
        return f(request, *args, **kwargs)

    return wrapper
