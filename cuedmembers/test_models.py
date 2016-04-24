from django.test import TestCase
from django.contrib.auth.models import User

from .models import Member

class MemberTestCase(TestCase):
    fixtures = ['test_users', 'test_members']

    def test_active_members(self):
        self.assertGreater(Member.objects.active().count(), 0)
        for o in Member.objects.active().all():
            self.assertTrue(o.is_active)

    def test_inactive_members(self):
        members = Member.objects.inactive()
        self.assertGreater(members.count(), 0)
        for o in members:
            self.assertFalse(o.is_active)

    def test_non_members(self):
        non_member_users = User.objects.filter(cued_member__isnull=True)
        self.assertGreater(non_member_users.count(), 0)
        for o in non_member_users:
            with self.assertRaises(Member.DoesNotExist):
                Member.objects.get(user=o)

    def test_have_crsids(self):
        for o in Member.objects.all():
            self.assertIsNotNone(o.crsid)
