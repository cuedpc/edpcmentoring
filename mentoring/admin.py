from django.contrib import admin
from .models import MentorshipRelationship

class MentorshipRelationshipAdmin(admin.ModelAdmin):
    list_display = ('description', 'mentor_crsid',
                    'mentee_crsid', 'is_active',
                    'started_on', 'ended_on')

    list_filter = ('is_active',)

    def mentor_crsid(self, obj):
        return obj.mentor.user.username

    def mentee_crsid(self, obj):
        return obj.mentee.user.username

    def description(self, obj):
        return '{} mentoring {}'.format(
            obj.mentor.user.get_full_name(),
            obj.mentee.user.get_full_name())

admin.site.register(MentorshipRelationship, MentorshipRelationshipAdmin)
