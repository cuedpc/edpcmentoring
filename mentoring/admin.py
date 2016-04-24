from django.contrib import admin

from .models import (
    StaffMember, MentorshipPreferences, MentorshipRelationship,
    Invitation, Meeting, MeetingAttendance, TrainingEvent
)

class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('crsid', 'full_name', 'division', 'is_active',
                    'arrived_on', 'departed_on', 'expected_departure_on')

    list_filter = ('arrived_on', 'departed_on', 'expected_departure_on')

    def get_queryset(self, request):
        return StaffMember.objects.get_queryset()

    def crsid(self, obj):
        return obj.user.username

    def full_name(self, obj):
        return obj.user.get_full_name()

class MentorshipRelationshipAdmin(admin.ModelAdmin):
    list_display = ('description', 'mentor_crsid',
                    'mentee_crsid', 'is_active',
                    'started_on', 'ended_on')

    def mentor_crsid(self, obj):
        return obj.mentor.user.username

    def mentee_crsid(self, obj):
        return obj.mentee.user.username

    def description(self, obj):
        return '{} mentoring {}'.format(
            obj.mentor.user.get_full_name(),
            obj.mentee.user.get_full_name())

admin.site.register(MentorshipRelationship, MentorshipRelationshipAdmin)

class MentorshipPreferencesAdmin(admin.ModelAdmin):
    list_display = ('crsid', 'full_name', 'is_seeking_mentor',
                    'is_seeking_mentee')

    def crsid(self, obj):
        return obj.staff_member.user.username

    def full_name(self, obj):
        return obj.staff_member.user.get_full_name()

admin.site.register(MentorshipPreferences, MentorshipPreferencesAdmin)

admin.site.register(StaffMember, StaffMemberAdmin)
admin.site.register(Invitation)
admin.site.register(Meeting)
admin.site.register(MeetingAttendance)
admin.site.register(TrainingEvent)

# Register your models here.
