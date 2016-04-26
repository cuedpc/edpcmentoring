import csv
from io import StringIO

from django.test import TestCase

from ..io import write_members_to_csv
from ..models import Member

class WriteMembersToCSVTestCase(TestCase):
    fixtures = ['cuedmembers/test_users', 'cuedmembers/test_members']

    def test_write_members_has_everyone(self):
        # Get a list of all *active* members
        qs = Member.objects.active().select_related('user')

        # Form a set of crsids from the active members
        crsids = set(obj.user.username for obj in qs)

        # Write CSV to a string
        with StringIO() as fobj:
            write_members_to_csv(fobj, qs)
            csv_contents = fobj.getvalue()

        # Read in CSV
        with StringIO(csv_contents) as fobj:
            reader = csv.DictReader(fobj)
            crsids_read = set(r.get('crsid') for r in reader)

        self.assertEqual(len(crsids), len(crsids_read))
        self.assertEqual(len(crsids.difference(crsids_read)), 0)
