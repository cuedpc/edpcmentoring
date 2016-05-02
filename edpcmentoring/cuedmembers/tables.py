import django_tables2 as tables

class MemberTable(tables.Table):
    crsid = tables.Column(
        accessor='username', verbose_name='CRSid',
        attrs={'th': {'style': 'width: 5em'}})
    name = tables.Column(
        accessor='get_full_name', verbose_name='Name',
        order_by=('last_name', 'first_name'))
    division = tables.Column(
        accessor='cued_member.research_group.division',
        verbose_name='Division',
        attrs={'th': {'style': 'width: 8em'}})
    research_group = tables.Column(
        accessor='cued_member.research_group',
        verbose_name='Research Group')
