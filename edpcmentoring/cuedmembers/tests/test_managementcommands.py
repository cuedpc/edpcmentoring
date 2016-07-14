import os
import shutil
import tempfile

from django.core.management import call_command
from django.test import TestCase

from ..models import Member

class TemporaryDirectoryTestCase(TestCase):
    """A TestCase which creates a temporary directory for each test whose path
    is available as the "tmpdir" attribute.

    """
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

class ImportCUEDMembersTestCase(TemporaryDirectoryTestCase):
    def test_csv_import(self):
        self.assertEqual(Member.objects.active().count(), 0)
        inpath = os.path.join(self.tmpdir, 'input.csv')
        with open(inpath, 'w') as f:
            f.write(MEMBERS_CSV_1)
        call_command('importcuedmembers', inpath)
        self.assertEqual(Member.objects.active().count(), 6)

    def test_import_deactivates_members(self):
        self.assertEqual(Member.objects.active().count(), 0)
        inpath = os.path.join(self.tmpdir, 'input.csv')
        with open(inpath, 'w') as f:
            f.write(MEMBERS_CSV_1)
        call_command('importcuedmembers', inpath)
        self.assertEqual(Member.objects.active().count(), 6)
        inpath = os.path.join(self.tmpdir, 'input.csv')
        with open(inpath, 'w') as f:
            f.write(MEMBERS_CSV_2)
        call_command('importcuedmembers', inpath)
        self.assertEqual(Member.objects.active().count(), 5)
        self.assertEqual(Member.objects.all().count(), 7)

    def test_email_domain(self):
        self.assertEqual(Member.objects.active().count(), 0)
        inpath = os.path.join(self.tmpdir, 'input.csv')
        with open(inpath, 'w') as f:
            f.write(MEMBERS_CSV_1)
        call_command('importcuedmembers', '-e', 'mailinator.com', inpath)
        self.assertEqual(Member.objects.active().count(), 6)
        u1 = Member.objects.filter(user__username='test0001').first().user
        self.assertEqual(u1.email, 'test0001@mailinator.com')


# Two CSV files with different sets of users

MEMBERS_CSV_1 = '''
crsid,status,surname,fnames,pref_name,room,phone,arrived,start_date,end_date,division,role_course,host_supervisor,research_group
test0001,,Klein,Alexandra Corrina,Alexandra,,,,,,C,,,Materials Engineering
test0002,,Herman,Verna Ibrahim Fletcher,Verna,,,,,,,,,
test0004,,Kihn,Clementine,Clementine,,,,,,C,,,Engineering Design
test0005,,Lindgren,Eric,Eric,,,,,,A,,,Turbomachinery
test0006,,Torphy,Shirleyann Arden Minerva,Minerva,,,,,,,,,
test0008,,Kling,Jorden,Jorden,,,,,,A,,,Turbomachinery
'''.strip()

MEMBERS_CSV_2 = '''
crsid,status,surname,fnames,pref_name,room,phone,arrived,start_date,end_date,division,role_course,host_supervisor,research_group
test0001,,Klein,Alexandra Corrina,Alexandra,,,,,,C,,,Materials Engineering
test0003,,Emmerich,Pleasant,Pleasant,,,,,,A,,,Turbomachinery
test0004,,Kihn,Clementine,Clementine,,,,,,C,,,Engineering Design
test0006,,Torphy,Shirleyann Arden Minerva,Minerva,,,,,,,,,
test0008,,Kling,Jorden,Jorden,,,,,,A,,,Turbomachinery
'''.strip()
