from django.core import mail
from django.test import TestCase

from cuedmembers.models import Member
from mentoring.models import Relationship
from matching.models import Invitation

class NewRelationshipTestCase(TestCase):
    fixtures = ['cuedmembers/test_users_and_members']

    def test_email_sent_on_new_relationship(self):
        """Creating a new relationship should notify the members."""
        u1, u2 = [m.user for m in Member.objects.active()[3:5]]
        self.assertEqual(Relationship.objects.filter(
            mentor=u1, mentee=u2).count(), 0)
        self.assertEqual(len(mail.outbox), 0)
        Relationship.objects.create(mentor=u1, mentee=u2)
        self.assertEqual(Relationship.objects.filter(
            mentor=u1, mentee=u2).count(), 1)
        self.assertEqual(len(mail.outbox), 2)

        mail_counts = {}
        for m in mail.outbox:
            for addr in m.to:
                mail_counts[addr] = mail_counts.get(addr, 0) + 1
        self.assertEqual(len(mail_counts), 2)
        self.assertEqual(mail_counts[u1.email], 1)
        self.assertEqual(mail_counts[u2.email], 1)

    def test_email_not_sent_on_new_inactive_relationship(self):
        """Creating a new inactive relationship should not notify the members.

        """
        u1, u2 = [m.user for m in Member.objects.active()[3:5]]
        self.assertEqual(Relationship.objects.filter(
            mentor=u1, mentee=u2).count(), 0)
        Relationship.objects.create(mentor=u1, mentee=u2, is_active=False)
        self.assertEqual(len(mail.outbox), 0)

    def test_email_not_sent_on_modifying_existing(self):
        """Re-saving an existing relationship should not notify the members.

        """
        u1, u2 = [m.user for m in Member.objects.active()[3:5]]
        self.assertEqual(Relationship.objects.filter(
            mentor=u1, mentee=u2).count(), 0)
        r = Relationship.objects.create(mentor=u1, mentee=u2)
        mail.outbox = []
        self.assertEqual(len(mail.outbox), 0)
        r.save()
        self.assertEqual(len(mail.outbox), 0)


    def test_email_sent_on_new_mentor_invite(self):
        """Creating a new invite should notify the invited member."""
        u1, u2 = [m.user for m in Member.objects.active()[3:5]]
        self.assertEqual(Invitation.objects.filter(
            mentor=u1, mentee=u2).count(), 0)
        self.assertEqual(len(mail.outbox), 0)
        Invitation.objects.create(mentor=u1, mentee=u2, created_by_id=u2.id, mentee_response='A')
        self.assertEqual(Invitation.objects.filter(
            mentor=u1, mentee=u2).count(), 1)
        self.assertEqual(len(mail.outbox), 1)

        mail_counts = {}
        for m in mail.outbox:
            for addr in m.to:
                mail_counts[addr] = mail_counts.get(addr, 0) + 1
        #self.assertEqual(len(mail_counts), 2)
        self.assertEqual(mail_counts[u1.email], 1)
        #self.assertEqual(mail_counts[u2.email], 1)

    def test_email_sent_on_mentor_invite_declined(self):
        """Creating a new invite and declining should notify the member."""
        u1, u2 = [m.user for m in Member.objects.active()[3:5]]
        self.assertEqual(Invitation.objects.filter(
            mentor=u1, mentee=u2).count(), 0)
        self.assertEqual(len(mail.outbox), 0)
        myinv = Invitation.objects.create(mentor=u1, mentee=u2, created_by_id=u2.id, mentee_response='A')
        self.assertEqual(Invitation.objects.filter(
            mentor=u1, mentee=u2).count(), 1)

        # Update the invite so that Mentor_response='D'!
	myinv.mentor_response='D'
        myinv.save()

        mail_counts = {}
        for m in mail.outbox:
            for addr in m.to:
                mail_counts[addr] = mail_counts.get(addr, 0) + 1
        #self.assertEqual(len(mail_counts), 2)
        #self.assertEqual(mail_counts[u1.email], 1)
        self.assertEqual(mail_counts[u2.email], 1)



    def test_email_sent_on_mentee_invite_declined(self):
        """Creating a new invite and declining should notify the member."""
        u1, u2 = [m.user for m in Member.objects.active()[3:5]]
        self.assertEqual(Invitation.objects.filter(
            mentor=u1, mentee=u2).count(), 0)
        self.assertEqual(len(mail.outbox), 0)
        myinv = Invitation.objects.create(mentor=u1, mentee=u2, created_by_id=u1.id, mentor_response='A')
        self.assertEqual(Invitation.objects.filter(
            mentor=u1, mentee=u2).count(), 1)

        # Update the invite to reflect mentee decline mentee_response='D'!
	myinv.mentee_response='D'
        myinv.save()

        mail_counts = {}
        for m in mail.outbox:
            for addr in m.to:
                mail_counts[addr] = mail_counts.get(addr, 0) + 1
        #self.assertEqual(len(mail_counts), 2) 
        self.assertEqual(mail_counts[u1.email], 1)
        #self.assertEqual(mail_counts[u2.email], 0)





