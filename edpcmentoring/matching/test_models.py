from __future__ import unicode_literals

from django.contrib.auth.models import Permission, User
from django.core.exceptions import ValidationError, PermissionDenied
from django.test import TestCase
from mentoring.models import Relationship
from matching.models import Invitation
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

        q1 = User.objects.filter(
            cued_member__isnull=False, is_superuser=True)
        self.superu = q[:1]


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

    def test_invite_as_mentor_is_accepted(self):
        # An invite created by a mentor is already accepted by them
        invite = Invitation(mentor=self.users[0], mentee=self.users[1],
                            created_by=self.users[0])
        invite.full_clean()
        invite.save()
        
        #There should be one active invite
        #self.assertEquals(Invitation.objects.filter(deactivated_on__isnull=False).count(),1)
        self.assertEquals(Invitation.objects.active().count(),1)

        self.assertIs(invite.mentor_response, Invitation.ACCEPT)
        self.assertIs(invite.mentee_response, '')

    def test_invite_as_mentee_is_accepted(self):
        # An invite created by a mentee is already accepted by them
        invite = Invitation(mentor=self.users[0], mentee=self.users[1],
                            created_by=self.users[1])
        invite.full_clean()
        self.assertIs(invite.mentor_response, '')
        self.assertIs(invite.mentee_response, Invitation.ACCEPT)

    def test_is_accepted_1(self):
        invite = Invitation(mentor=self.users[0], mentee=self.users[1],
                            created_by=self.users[1])
        invite.full_clean()
        assert not invite.is_accepted()
        invite.mentor_response = Invitation.ACCEPT
        assert invite.is_accepted()

    def test_is_accepted_2(self):
        invite = Invitation(mentor=self.users[0], mentee=self.users[1],
                            created_by=self.users[0])
        invite.full_clean()
        assert not invite.is_accepted()
        invite.mentee_response = Invitation.ACCEPT
        assert invite.is_accepted()

    def test_creates_relationship(self):
        invite = Invitation(mentor=self.users[0], mentee=self.users[1],
                            created_by=self.users[0])
        invite.mentee_response = Invitation.ACCEPT
        invite.full_clean()

        n_relationships = Relationship.objects.filter(
            mentor=invite.mentor, mentee=invite.mentee).count()
        self.assertEqual(n_relationships, 0)
        self.assertTrue(invite.is_active())
        invite.save()
        n_relationships = Relationship.objects.filter(
            mentor=invite.mentor, mentee=invite.mentee).count()
        self.assertEqual(n_relationships, 1)
        self.assertFalse(invite.is_active())

    def test_needs_acceptance_to_create(self):
        invite = Invitation(mentor=self.users[0], mentee=self.users[1],
                            created_by=self.users[0])
        invite.full_clean()

        n_relationships = Relationship.objects.filter(
            mentor=invite.mentor, mentee=invite.mentee).count()
        self.assertEqual(n_relationships, 0)
        self.assertTrue(invite.is_active())
        invite.save()
        n_relationships = Relationship.objects.filter(
            mentor=invite.mentor, mentee=invite.mentee).count()
        self.assertEqual(n_relationships, 0)
        self.assertTrue(invite.is_active())

    def test_deactivate(self):
        invite = Invitation(mentor=self.users[0], mentee=self.users[1],
                            created_by=self.users[0])
        invite.full_clean()
        self.assertTrue(invite.is_active())
        invite.deactivate()
        self.assertFalse(invite.is_active())

    def test_deactivate_does_not_create_relationship(self):
        invite = Invitation(mentor=self.users[0], mentee=self.users[1],
                            created_by=self.users[0])
        invite.full_clean()
        self.assertTrue(invite.is_active())
        invite.deactivate()
        invite.save()
        self.assertFalse(invite.is_active())
        n_relationships = Relationship.objects.filter(
            mentor=invite.mentor, mentee=invite.mentee).count()
        self.assertEqual(n_relationships, 0)

    def test_mentee_respond_decline(self):
        invite = Invitation(mentor=self.users[0], mentee=self.users[1],
                            created_by=self.users[0])
        self.assertTrue(invite.is_active())
        invite.full_clean()
        invite.respond(invite.mentee, False)
        invite.save()
        self.assertFalse(invite.is_active())
        self.assertFalse(invite.is_accepted())

    def test_mentor_respond_decline(self):
        invite = Invitation(mentor=self.users[0], mentee=self.users[1],
                            created_by=self.users[1])
        self.assertTrue(invite.is_active())
        invite.full_clean()
        invite.respond(invite.mentor, False)
        invite.save()
        self.assertFalse(invite.is_active())
        self.assertFalse(invite.is_accepted())

    def test_mentee_respond_accept(self):
        invite = Invitation(mentor=self.users[0], mentee=self.users[1],
                            created_by=self.users[0])
        self.assertTrue(invite.is_active())
        invite.full_clean()
        invite.respond(invite.mentee, True)
        invite.save()
        self.assertFalse(invite.is_active())
        self.assertTrue(invite.is_accepted())

    def test_mentor_respond_accept(self):
        invite = Invitation(mentor=self.users[0], mentee=self.users[1],
                            created_by=self.users[1])
        self.assertTrue(invite.is_active())
        invite.full_clean()
        invite.respond(invite.mentor, True)
        invite.save()
        self.assertFalse(invite.is_active())
        self.assertTrue(invite.is_accepted())

    def test_matchmaker_respond_accept(self):
        invite = Invitation(mentor=self.users[0], mentee=self.users[1],
                            created_by=self.users[1])
        self.assertTrue(invite.is_active())
        invite.full_clean()
       
        invite.respond(self.superu[0], True)
        invite.save()
        self.assertFalse(invite.is_active())
        self.assertTrue(invite.is_accepted())

    def test_matchmaker_respond_decline(self):
        invite = Invitation(mentor=self.users[0], mentee=self.users[1],
                            created_by=self.users[1])
        self.assertTrue(invite.is_active())
        invite.full_clean()
        invite.respond(self.superu[0], False)
        invite.save()
        self.assertFalse(invite.is_active())
        self.assertFalse(invite.is_accepted())


    def test_permission_to_respond(self):
        invite = Invitation(mentor=self.users[0], mentee=self.users[1],
                            created_by=self.users[1])
        self.assertTrue(invite.is_active())
        invite.full_clean()
        #invite.respond(self.users[2], False)
        #invite.save()
        #self.assertFalse(invite.is_active())
        #self.assertFalse(invite.is_accepted())
        with self.assertRaises(PermissionDenied):
            invite.respond(self.users[2], False)
            invite.save()



    def test_mentor_cannotbe_mentee(self):
        invite = Invitation(mentor=self.users[0], mentee=self.users[0],
                            created_by=self.users[0])
        #invite.full_clean()
        #invite.respond(self.users[2], False)
        #invite.save()
        #self.assertFalse(invite.is_active())
        #self.assertFalse(invite.is_accepted())
	with self.assertRaises(ValidationError):
            invite.full_clean()
            #invite.respond(self.users[2], False)
            #invite.save()








