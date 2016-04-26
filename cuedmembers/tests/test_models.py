from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Member

class MemberTestCase(TestCase):
    fixtures = ['cuedmembers/test_users_and_members']

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
        non_member_users = get_user_model().objects.filter(
            cued_member__isnull=True)
        self.assertGreater(non_member_users.count(), 0)
        for o in non_member_users:
            with self.assertRaises(Member.DoesNotExist):
                Member.objects.get(user=o)

    def test_have_crsids(self):
        for o in Member.objects.all():
            self.assertIsNotNone(o.crsid)

    def test_create_from_existing_user(self):
        # Find a user who is not currently a member
        u = get_user_model().objects.filter(
            cued_member__isnull=True).first()

        # Auto-creating a member should succeed even if the information is of
        # little use.
        m, _ = Member.objects.update_or_create_by_crsid(
            u.username, dict(first_name='XXXX', is_active=True))
        self.assertEqual(m.user.username, u.username)
        self.assertEqual(m.user.first_name, 'XXXX')

        # Check the member was created
        self.assertIsNot(Member.objects.active().filter(
            user__username=u.username).first(), None)

    def test_create_with_new_user(self):
        # There is no user called 'nosuch1'?
        User = get_user_model()
        crsid = 'nosuch1'

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username=crsid)

        # Create a new member
        m, _ = Member.objects.update_or_create_by_crsid(
            crsid,
            dict(first_name='Joe', last_name='Bloggs',
                 first_names='Mr. J.', email='{}@example.com'.format(crsid))
        )

        # Check user password is unavailable
        self.assertFalse(m.user.has_usable_password())

        # Check that the user is active (the default)
        Member.objects.active().filter(user__username=crsid).first()
