def staff_member(request):
    """Inject the current staff member into the request if one is available."""
    sm = getattr(request, 'staff_member')
    if sm is not None:
        return {'staff_member': sm}
    return {}
