from django.contrib.auth.models import Permission, User
from django.test import TestCase

from .models import Invitation
from .forms import InvitationResponseForm

class InvitationResponseTestCase(TestCase):
    fixtures = ['cuedmembers/test_users_and_members']

    def setUp(self):
        q = User.objects.filter(
            cued_member__isnull=False, is_superuser=False, is_staff=False)
        self.users = q[:10]
        invite = Invitation(mentor=self.users[0], mentee=self.users[1],
                            created_by=self.users[3])

        # Add the required permission to the creator
        invite.created_by.user_permissions.add(
            Permission.objects.get(codename='add_invitation')
        )

        # Refresh user permissions (see Permission caching docs)
        invite.created_by = User.objects.get(pk=invite.created_by.id)
        invite.full_clean()
        invite.save()

        self.invite = Invitation.objects.get(pk=invite.id)

        self.valid_data = {
            'user': self.invite.mentor.id,
            'response': Invitation.ACCEPT,
        }

    def test_valid_data(self):
        f = InvitationResponseForm(self.valid_data, instance=self.invite)
        self.assertTrue(f.is_valid())

    def test_invite_should_be_active(self):
        self.invite.deactivate()
        self.invite.save()
        f = InvitationResponseForm(self.valid_data, instance=self.invite)
        self.assertFalse(f.is_valid())

    def test_user_is_mentor(self):
        data = {}
        data.update(self.valid_data)
        data['user'] = self.invite.mentor.id
        f = InvitationResponseForm(data, instance=self.invite)
        self.assertTrue(f.is_valid())

    def test_user_is_mentee(self):
        data = {}
        data.update(self.valid_data)
        data['user'] = self.invite.mentee.id
        f = InvitationResponseForm(data, instance=self.invite)
        self.assertTrue(f.is_valid())

    def test_user_is_someone_else(self):
        data = {}
        data.update(self.valid_data)
        data['user'] = self.users[4].id
        f = InvitationResponseForm(data, instance=self.invite)
        self.assertFalse(f.is_valid())
