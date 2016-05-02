from crispy_forms.helper import FormHelper
from django.db.models import Sum, When, Case, Value, IntegerField
from django.db.models.functions import Coalesce
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.base import TemplateView
import django_filters as filters
import django_tables2 as tables

from cuedmembers.models import Division
from cuedmembers.tables import MemberTable
from frontend.layout import Submit

class MatchmakeFilter(filters.FilterSet):
    division = filters.ModelChoiceFilter(
        name='cued_member__research_group__division',
        lookup_expr='exact', distinct=True,
        queryset=Division.objects.order_by('letter'))

    max_mentors_count = filters.NumberFilter(
        name='mentors_count',
        label='Maximum number of mentors',
        lookup_expr='lte')

class MatchmakeTable(MemberTable):
    mentors_count = tables.Column(
        accessor='mentors_count', verbose_name='# Mentors',
        attrs={'th': {'style': 'width: 8em'}})

    class Meta(object):
        attrs = {
            'class': ('campl-table-bordered campl-table-striped campl-table '
                      'campl-vertical-stacking-table'),
        }

class MatchmakeView(PermissionRequiredMixin, TemplateView):
    http_method_names = ['get', 'head', 'options']
    permission_required = 'matching.matchmake'
    raise_exception = True
    template_name = 'matching/matchmake.html'

    def get_context_data(self, **kwargs):
        # Get a list of users who are active CUED members seeking mentors
        seekers = get_user_model().objects.\
            filter(cued_member__is_active=True,
                   mentorship_preferences__is_seeking_mentor=True).\
            select_related('cued_member',
                           'cued_member__research_group',
                           'cued_member__research_group__division')

        # We want to annotate each seeker with the number of active mentee
        # relationships they are currently a part of
        seekers = seekers.\
            annotate(mentors_count=Coalesce(Sum(
                Case(When(mentee_relationships__is_active=True, then=Value(1)),
                     When(mentee_relationships__is_active=False, then=Value(0)),
                     output_field=IntegerField())
            ), 0))

        f = MatchmakeFilter(self.request.GET, queryset=seekers)

        helper = FormHelper(f.form)
        helper.html5_required = True
        helper.error_text_inline = False
        helper.form_action = ""
        helper.form_method = "get"
        helper.add_input(Submit("submit", "Update filter"))
        f.form.helper = helper

        table = MatchmakeTable(
            f.qs, order_by='crsid', empty_text='No people match this filter')
        tables.RequestConfig(
            self.request, paginate=False).configure(table)

        return {'table': table, 'filter': f}
