from django.contrib import admin
from .models import Preferences, Invitation

class PreferencesAdmin(admin.ModelAdmin):
    list_display = ('crsid', 'full_name', 'is_seeking_mentor',
                    'is_seeking_mentee')

    def crsid(self, obj):
        return obj.user.username

    def full_name(self, obj):
        return obj.user.get_full_name()

admin.site.register(Preferences, PreferencesAdmin)

admin.site.register(Invitation)
