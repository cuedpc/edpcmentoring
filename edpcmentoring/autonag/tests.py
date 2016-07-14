from django.core import mail
from django.test import TestCase

from cuedmembers.models import Member
from mentoring.models import Relationship

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
