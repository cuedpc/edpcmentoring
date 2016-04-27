from contextlib import closing
import csv

# Python 2 does indeed have io.StringIO but it only accepts unicode input which
# is incompatible with the csv module (yay, unicode!). Work around this by
# trying to import the old-style StringIO module from Python 2 and, if this
# fails, try the new-style io.StringIO.
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import random

from django.test import TestCase

from ..io import write_members_to_csv, read_members_from_csv
from ..models import Member

class WriteMembersToCSVTestCase(TestCase):
    fixtures = ['cuedmembers/test_users_and_members']

    def test_write_members_has_everyone(self):
        # Get a list of all *active* members
        qs = Member.objects.active().select_related('user')

        # Form a set of crsids from the active members
        crsids = set(obj.user.username for obj in qs)

        # Write CSV to a string
        with closing(StringIO()) as fobj:
            write_members_to_csv(fobj, qs)
            csv_contents = fobj.getvalue()

        # Read in CSV
        with closing(StringIO(csv_contents)) as fobj:
            reader = csv.DictReader(fobj)
            crsids_read = set(r.get('crsid') for r in reader)

        self.assertEqual(len(crsids), len(crsids_read))
        self.assertEqual(len(crsids.difference(crsids_read)), 0)

class ReadMembersFromCSVTestCase(TestCase):
    fixtures = ['cuedmembers/test_users_and_members']

    def setUp(self):
        self.assertGreater(Member.objects.count(), 0)

        # Write all current members as CSV to a string
        with closing(StringIO()) as fobj:
            write_members_to_csv(fobj, Member.objects.all())
            csv_contents = fobj.getvalue()

        # Parse CSV into row dictionaries and fieldnames
        with closing(StringIO(csv_contents)) as fobj:
            reader = csv.DictReader(fobj)
            self.field_names = reader.fieldnames
            self.rows = list(reader)

        # Remove all members from the DB
        Member.objects.all().delete()

    def test_read_members_once(self):
        """
        Check the simple case of reading a CSV into the database when empty.

        """
        self.assertEqual(Member.objects.count(), 0)
        self.assert_read_members(self.rows)
        self.assertEqual(Member.objects.inactive().count(), 0)

    def test_read_members_repeatedly(self):
        """
        Check the more complex case of updating the database with a random
        subset of rows more than once.

        """
        self.assertEqual(Member.objects.count(), 0)
        iteration_count = 10
        for _ in range(iteration_count):
            row_count = random.randint(len(self.rows)>>1, len(self.rows))
            row_subset = random.sample(self.rows, row_count)
            self.assert_read_members(row_subset)
        self.assertGreater(Member.objects.inactive().count(), 0)

    def test_changes_first_name(self):
        for row_idx in range(len(self.rows), 20):
            self.assert_read_members_changes_user_field(
                row_idx, 'pref_name', 'first_name')

    def test_changes_last_name(self):
        for row_idx in range(len(self.rows), 20):
            self.assert_read_members_changes_user_field(
                row_idx, 'surname', 'last_name')

    def assert_read_members_changes_user_field(self, row_idx, csvname, fieldname,
                                               new_value='XXXXXX'):
        row_to_change = self.rows[row_idx]
        crsid = row_to_change['crsid']
        self.assert_read_members(self.rows)
        self.assertNotEqual(
            getattr(Member.objects.get(user__username=crsid).user, fieldname),
            new_value)
        row_to_change[csvname] = new_value
        self.assert_read_members(self.rows)
        self.assertEqual(
            getattr(Member.objects.get(user__username=crsid).user, fieldname),
            new_value)

    def assert_read_members(self, rows):
        """
        Reads members into the database from a CSV file containing the passed
        rows. Asserts that the active member crsids match those in the rows.

        """
        read_members_from_csv(csv_file_from_rows(self.field_names, rows))

        # Check that the active user crsids are only those in the rows we
        # passed.
        qs = Member.objects.active().select_related('user')
        expected_crsids = set(r.get('crsid') for r in rows)
        got_crsids = set(m.user.username for m in qs)

        self.assertEqual(len(expected_crsids ^ got_crsids), 0)

def csv_file_from_rows(field_names, rows):
    """Return a file object which, when read from, will give a CSV file with the
    specified field names and rows. Each row should be a dictionary as with
    csv.DictWriter.

    """
    with closing(StringIO()) as fobj:
        writer = csv.DictWriter(fobj, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(rows)
        return StringIO(fobj.getvalue())
