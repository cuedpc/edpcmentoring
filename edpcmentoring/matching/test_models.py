from django.contrib.auth.models import Permission, User
from django.core.exceptions import ValidationError
from django.test import TestCase
from cuedmembers.models import Member

from .models import Preferences, Invitation

class PreferencesTestCase(TestCase):
    fixtures = ['cuedmembers/test_users_and_members']

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

class InvitationTestCase(TestCase):
    fixtures = ['cuedmembers/test_users_and_members']

    def setUp(self):
        q = User.objects.filter(
            cued_member__isnull=False, is_superuser=False, is_staff=False)
        self.users = q[:10]

    def test_no_matchmaking_without_permission(self):
        invite = Invitation(mentor=self.users[0], mentee=self.users[1],
                            created_by=self.users[3])

        # A user cannot create an invite where they're not a mentor or mentee
        assert not invite.created_by.has_perm('matching.add_invitation')
        with self.assertRaises(ValidationError):
            invite.full_clean()

        # Add the required permission
        invite.created_by.user_permissions.add(
            Permission.objects.get(codename='add_invitation')
        )

        # Refresh user permissions (see Permission caching docs)
        invite.created_by = User.objects.get(pk=invite.created_by.id)
        assert invite.created_by.has_perm('matching.add_invitation')

        # Invite should now validate
        invite.full_clean()

    def test_invite_as_mentor(self):
        invite = Invitation(mentor=self.users[0], mentee=self.users[1],
                            created_by=self.users[0])

        # A user may invite a mentee even with no add permission
        assert not invite.created_by.has_perm('matching.add_invitation')
        invite.full_clean()

    def test_invite_as_mentee(self):
        invite = Invitation(mentor=self.users[0], mentee=self.users[1],
                            created_by=self.users[1])

        # A user may invite a mentor even with no add permission
        assert not invite.created_by.has_perm('matching.add_invitation')
        invite.full_clean()
