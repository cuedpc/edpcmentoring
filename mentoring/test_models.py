from django.test import TestCase
from django.contrib.auth.models import User

from .models import StaffMember

class StaffMemberTestCase(TestCase):
    fixtures = ['staff_members']

    def setUp(self):
        self.non_staff_user = User.objects.filter(
            staffmember__isnull=True).first()
        self.departed_staff_user = StaffMember.objects.filter(
            departed_on__isnull=False).first().user

    def test_current_staff_members(self):
        self.assertGreater(StaffMember.current_members.count(), 0)
        for o in StaffMember.current_members.all():
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

