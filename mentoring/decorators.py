from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def staff_member_required(f):
    """A decorator which wraps login_required additionally checking that the
    logged in user is a StaffMember. If not, a 404 is raised.

    """
    # Wrap function with login_required
    f = login_required(f)

    @wraps(f)
    def wrapper(request, *args, **kwargs):
        user = getattr(request, 'user')
        staff_member = getattr(request, 'staff_member')
        if user is not None and user.is_authenticated():
            if staff_member is None or not staff_member.is_current:
                raise PermissionDenied()
        return f(request, *args, **kwargs)

    return wrapper
