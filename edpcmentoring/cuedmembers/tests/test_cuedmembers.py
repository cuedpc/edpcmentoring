"""
Tests for functionality in the top-level cuedmembers module.

"""
from django.test import TestCase

from cuedmembers import get_member_group

class GetMemberGroupTestCase(TestCase):
    def test_creates_group(self):
        g = get_member_group()
        self.assertEqual(g.name, 'CUED Members')

    def test_returns_same_created_group_twice(self):
        g1 = get_member_group()
        g2 = get_member_group()
        self.assertEqual(g1.id, g2.id)
