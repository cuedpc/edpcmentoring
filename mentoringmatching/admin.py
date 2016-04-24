from django.contrib import admin
from .models import MentorshipPreferences, Invitation

class MentorshipPreferencesAdmin(admin.ModelAdmin):
    list_display = ('crsid', 'full_name', 'is_seeking_mentor',
                    'is_seeking_mentee')

    def crsid(self, obj):
        return obj.staff_member.user.username

    def full_name(self, obj):
        return obj.staff_member.user.get_full_name()

admin.site.register(MentorshipPreferences, MentorshipPreferencesAdmin)

admin.site.register(Invitation)
