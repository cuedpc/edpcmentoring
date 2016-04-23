from django.test import TestCase
from django.contrib.auth.models import User

from .models import StaffMember, MentorshipPreferences

class StaffMemberTestCase(TestCase):
    fixtures = ['staff_members']

    def setUp(self):
        self.non_staff_user = User.objects.filter(
            staffmember__isnull=True).first()
        self.departed_staff_user = StaffMember.objects.filter(
            departed_on__isnull=False).first().user

    def test_current_staff_members(self):
        self.assertGreater(StaffMember.objects.current().count(), 0)
        for o in StaffMember.objects.current().all():
            self.assertIsNone(o.departed_on)
            self.assertTrue(o.is_current)

    def test_departed_staff_members(self):
        members = StaffMember.objects.filter(departed_on__isnull=False)
        self.assertGreater(members.count(), 0)
        for o in members:
            self.assertFalse(o.is_current)

    def test_non_staff_members(self):
        non_staff_users = User.objects.filter(staffmember__isnull=True)
        self.assertGreater(non_staff_users.count(), 0)
        for o in non_staff_users:
            with self.assertRaises(StaffMember.DoesNotExist):
                StaffMember.objects.get(user=o)

    def test_preferences(self):
        staff_member = StaffMember.objects.current().first()

        # Check that there is not currently a mentorship preferences instance
        # for this user.
        with self.assertRaises(MentorshipPreferences.DoesNotExist):
            MentorshipPreferences.objects.get(staff_member=staff_member)

        # Mentorship preferences should auto create
        prefs = staff_member.mentorship_preferences

        # Now there should be an object
        MentorshipPreferences.objects.get(staff_member=staff_member)

        self.assertFalse(prefs.is_seeking_mentor)
        self.assertFalse(prefs.is_seeking_mentee)
        self.assertEqual(prefs.mentor_requirements, '')
        self.assertEqual(prefs.mentee_requirements, '')

