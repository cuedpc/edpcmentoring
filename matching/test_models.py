from django.test import TestCase
from cuedmembers.models import Member

from .models import Preferences

class PreferencesTestCase(TestCase):
    fixtures = ['cuedmembers/test_users', 'cuedmembers/test_members']

    def test_preferences(self):
        member = Member.objects.active().first()
        user = member.user

        # Check that there is not currently a mentorship preferences instance
        # for this user.
        with self.assertRaises(Preferences.DoesNotExist):
            Preferences.objects.get(user=member.user)

        #  preferences should auto create
        prefs = user.mentorship_preferences

        # Now there should be an object
        Preferences.objects.get(user=member.user)

        self.assertFalse(prefs.is_seeking_mentor)
        self.assertFalse(prefs.is_seeking_mentee)
        self.assertEqual(prefs.mentor_requirements, '')
        self.assertEqual(prefs.mentee_requirements, '')

