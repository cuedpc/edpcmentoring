from django.contrib import admin
from .models import Relationship, Meeting

class RelationshipAdmin(admin.ModelAdmin):
    list_display = ('description', 'mentor_crsid',
                    'mentee_crsid', 'is_active',
                    'started_on', 'ended_on')

    list_filter = ('is_active',)

    def mentor_crsid(self, obj):
        return obj.mentor.username

    def mentee_crsid(self, obj):
        return obj.mentee.username

    def description(self, obj):
        return '{} mentoring {}'.format(
            obj.mentor.get_full_name(),
            obj.mentee.get_full_name())

admin.site.register(Relationship, RelationshipAdmin)

class MeetingAdmin(admin.ModelAdmin):
    list_display = ('held_on', 'approximate_duration', 'mentor',
                    'mentee')

    def mentor(self, obj):
        return obj.relationship.mentor

    def mentee(self, obj):
        return obj.relationship.mentee

admin.site.register(Meeting, MeetingAdmin)
