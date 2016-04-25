from django.contrib import admin

from .models import Member, Status, ResearchGroup

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
    list_display = ('member', 'role', 'start_on', 'end_on')
    list_filter = ('role',)

admin.site.register(Status, StatusAdmin)

class ResearchGroupAdmin(admin.ModelAdmin):
    list_display = ('description', 'division')
    lift_filter = ('division')

admin.site.register(ResearchGroup, ResearchGroupAdmin)
