from django.contrib import admin
from .models import Meeting

class MeetingAdmin(admin.ModelAdmin):
    list_display = ('get_mentor',)

admin.site.register(Meeting, MeetingAdmin)
