from django import template

register = template.Library()

@register.inclusion_tag('frontend/tag/member_table.html')
def member_table(members):
    """
    A table of CUED members showing CRSid, name, division and research groups.
    Takes a sequence of cuedmembers.Member.

    """
    return {'members': members}

@register.inclusion_tag('frontend/tag/member_table.html')
def single_member_table(member):
    """
    Like member_table() except that only a single cuedmembers.Member is taken.

    """
    return {'members': [member]}
