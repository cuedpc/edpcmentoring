from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import Member

def member_required(f):
    """A decorator which wraps login_required additionally checking that the
    logged in user is an active member of CUED.

    If the user is logged in but not a member of CUED, or is an inactive member,
    a PermissionDenied exception is raised.

    """
    @wraps(f)
    @login_required
    def wrapper(request, *args, **kwargs):
        # Attribute will always be on request because this wrapper is decorated
        # with login_required.
        user = request.user
        assert user.is_authenticated()

        try:
            cued_member = user.cued_member
        except Member.DoesNotExist:
            raise PermissionDenied()

        if not cued_member.is_active:
            raise PermissionDenied()

        return f(request, *args, **kwargs)

    return wrapper

def matchmaker_required(f):
    """
    A decorator to require that the user has the matchmaker permission

    If the user is logged in but not a member of CUED, or is an inactive member,
    a PermissionDenied exception is raised.

    """
    @wraps(f)
    @login_required
    def wrapper(request, *args, **kwargs):
        # Attribute will always be on request because this wrapper is decorated
        # with login_required.
        user = request.user
        assert user.is_authenticated()

        try:
            is_matchmaker = user.has_perm('matching.matchmake')
        except :
            raise PermissionDenied()

        if not is_matchmaker:
            raise PermissionDenied()

        return f(request, *args, **kwargs)

    return wrapper

    
