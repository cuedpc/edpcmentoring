def cued_member(request):
    """Inject the current CUED member into the request if one is available."""
    member = getattr(request, 'cued_member')
    if member is not None:
        return {'cued_member': member}
    return {}
