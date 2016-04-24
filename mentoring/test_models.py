from django.test import TestCase
from django.contrib.auth.models import User
from cuedmembers.models import Member

from .models import MentorshipPreferences

class MentorshipPreferencesTestCase(TestCase):
    fixtures = ['test_users', 'test_members']

    def test_preferences(self):
        member = Member.objects.active().first()

        # Check that there is not currently a mentorship preferences instance
        # for this user.
        with self.assertRaises(MentorshipPreferences.DoesNotExist):
            MentorshipPreferences.objects.get(member=member)

        # Mentorship preferences should auto create
        prefs = member.mentorship_preferences

        # Now there should be an object
        MentorshipPreferences.objects.get(member=member)

        self.assertFalse(prefs.is_seeking_mentor)
        self.assertFalse(prefs.is_seeking_mentee)
        self.assertEqual(prefs.mentor_requirements, '')
        self.assertEqual(prefs.mentee_requirements, '')

