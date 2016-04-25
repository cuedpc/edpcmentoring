from django.contrib import admin

from .models import Member, Status

class MemberAdmin(admin.ModelAdmin):
    list_display = ('crsid', 'full_name', 'is_active',
                    'division', 'research_group',
                    'arrived_on')

    list_filter = ('is_active', 'division', 'arrived_on')

    def get_queryset(self, request):
        return Member.objects.get_queryset()

    def full_name(self, obj):
        return obj.user.get_full_name()

admin.site.register(Member, MemberAdmin)

class StatusAdmin(admin.ModelAdmin):
    list_display = ('member', 'role', 'start_on', 'end_on')
    list_filter = ('role',)

admin.site.register(Status, StatusAdmin)
