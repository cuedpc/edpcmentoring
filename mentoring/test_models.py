from django.core.exceptions import ValidationError
from django.test import TestCase

from cuedmembers.models import Member
from .models import Relationship

class RelationshipActiveInactiveTestCase(TestCase):
    fixtures = ['cuedmembers/test_users_and_members']

    def setUp(self):
        # Pull two active members from the database
        m1, m2 = Member.objects.active().all()[2:4]

        # Create relationship between them
        self.active_relationship = Relationship(
            mentor=m1.user, mentee=m2.user, is_active=True)
        self.active_relationship.save()

        # Create inactive relationship between them
        self.inactive_relationship = Relationship(
            mentor=m1.user, mentee=m2.user, is_active=False)
        self.inactive_relationship.save()

        self.mentor = m1.user
        self.mentee = m2.user

    def test_active(self):
        relationships = Relationship.objects.active().filter(
            mentor=self.mentor).all()
        self.assertEqual(len(relationships), 1)
        self.assertEqual(relationships[0].id, self.active_relationship.id)

    def test_inactive(self):
        relationships = Relationship.objects.inactive().filter(
            mentor=self.mentor).all()
        self.assertEqual(len(relationships), 1)
        self.assertEqual(relationships[0].id, self.inactive_relationship.id)

class RelationshipTestCase(TestCase):
    fixtures = ['cuedmembers/test_users_and_members']

    def test_cannot_have_identical_mentor_and_mentee(self):
        m = Member.objects.all()[0]
        u = m.user
        r = Relationship(mentor=u, mentee=u)
        with self.assertRaises(ValidationError):
            r.full_clean()
