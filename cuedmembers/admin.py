from django.contrib import admin

from .models import Member

class MemberAdmin(admin.ModelAdmin):
    list_display = ('crsid', 'full_name', 'division', 'is_active',
                    'arrived_on', 'last_inactive_on')

    list_filter = ('is_active', 'arrived_on')

    def get_queryset(self, request):
        return Member.objects.get_queryset()

    def full_name(self, obj):
        return obj.user.get_full_name()

admin.site.register(Member, MemberAdmin)
