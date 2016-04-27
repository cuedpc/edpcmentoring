from django import template

register = template.Library()

@register.inclusion_tag('frontend/tag/member_table.html')
def member_table(users):
    """
    A table of CUED members showing CRSid, name, division and research groups.
    Takes a sequence of users. This tag will follow the cued_member,
    cued_member__research_group and cued_member__research_group__division
    relations and so it's highly advisable to use select_related on any
    queryset.

    """
    return {'users': users}

@register.inclusion_tag('frontend/tag/member_table.html')
def single_member_table(user):
    """
    Like member_table() except that only a single user is taken.

    """
    return {'users': [user]}
