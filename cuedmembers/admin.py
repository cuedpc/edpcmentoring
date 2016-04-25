from django.contrib import admin

from .models import Member, Status, ResearchGroup, Division

class MemberAdmin(admin.ModelAdmin):
    list_display = ('crsid', 'full_name', 'division', 'research_group',
                    'is_active', 'arrived_on')

    list_filter = ('is_active', 'arrived_on')

    def full_name(self, obj):
        return obj.user.get_full_name()

    def division(self, obj):
        if obj.research_group is None:
            return None
        return obj.research_group.division

admin.site.register(Member, MemberAdmin)

class StatusAdmin(admin.ModelAdmin):
    list_display = ('member', 'status', 'start_on', 'end_on')
    list_filter = ('status',)

admin.site.register(Status, StatusAdmin)

class ResearchGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'division')

    def get_queryset(self, request):
        return ResearchGroup.objects.order_by('division__letter', 'name')

admin.site.register(ResearchGroup, ResearchGroupAdmin)

class DivisionAdmin(admin.ModelAdmin):
    list_display = ('letter', 'name')

    def get_queryset(self, request):
        return Division.objects.order_by('letter')

admin.site.register(Division, DivisionAdmin)
