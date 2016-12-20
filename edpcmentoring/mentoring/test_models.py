from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from cuedmembers.models import Member
from .models import Relationship

class RelationshipActiveInactiveTestCase(TestCase):
    fixtures = ['cuedmembers/test_users_and_members']

    def setUp(self):
        # Pull active members from the database
        m1, m2, m3 = Member.objects.active().all()[:3]

        # Create relationship between them
        self.active_relationship = Relationship(
            mentor=m1.user, mentee=m2.user, is_active=True)
        self.active_relationship.save()

        # Create inactive relationship between them
        self.inactive_relationship = Relationship(
            mentor=m1.user, mentee=m3.user, is_active=False)
        self.inactive_relationship.save()

    def test_active(self):
        relationships = Relationship.objects.active().all()
        self.assertEqual(len(relationships), 1)
        self.assertEqual(relationships[0].id, self.active_relationship.id)

    def test_inactive(self):
        relationships = Relationship.objects.inactive().all()
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

    def test_cannot_have_non_unique_mentor_mentee(self):
        u1, u2 = [m.user for m in Member.objects.all()[:2]]

        # should succeed
        r = Relationship(mentor=u1, mentee=u2, is_active=True)
        r.save()

        # should succeed (multiple inactive relationships allowed)
        r = Relationship(mentor=u1, mentee=u2, is_active=False)
        r.clean()


        # should succeed (multiple inactive relationships allowed)
        r = Relationship(mentor=u1, mentee=u2, is_active=False)
        r.clean()

       

        # should fail due to non uniqueness
        r = Relationship(mentor=u1, mentee=u2, is_active=True)
        with self.assertRaises(ValidationError):
            r.clean()

