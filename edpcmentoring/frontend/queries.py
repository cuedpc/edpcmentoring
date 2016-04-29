def select_member_details(qs):
    """
    Returns the passed User queryset calling select_related to select the
    complete CUED membership details for a user.

    """
    return qs.all().select_related(
        'cued_member',
        'cued_member__research_group',
        'cued_member__research_group__division',
    )
