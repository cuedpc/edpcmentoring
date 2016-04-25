"""
Create fake CUED members and users in the database.

Run via:

    manage.py runscript cuedmembers_generate_test_fixtures

"""
import datetime
import random

from django.contrib.auth.models import User
from django.utils import timezone
from faker import Faker

from cuedmembers.models import Member, Status, ResearchGroup

STATUSES = [Status.VISITOR, Status.POSTGRAD, Status.STAFF]

def sample_person(fake):
    """Use the faker to sample a fake person. Returns a dictionary containing
    first_name, last_name, first_names and research_group.

    """
    # For the sake of database testing, gender is binary when it comes to
    # generating names and prefixes.
    if random.random() < 0.5:
        make_first_name = fake.first_name_female
        make_prefix = fake.prefix_female
    else:
        make_first_name = fake.first_name_male
        make_prefix = fake.prefix_male

    first_name_list = [make_first_name() for _ in range(random.randint(1, 4))]
    prefix = make_prefix()
    first_name = random.choice(first_name_list)
    first_names = prefix + ' ' + ' '.join(n[:1]+'.' for n in first_name_list)
    last_name = fake.last_name()

    if random.random() < 0.2:
        research_group = None
    else:
        division = random.choice(ResearchGroup.objects.divisions())
        research_group = random.choice(
            ResearchGroup.objects.filter(division=division))

    return dict(
        first_name=first_name, last_name=last_name,
        first_names=first_names, research_group=research_group)

def sample_date_after(whence=None):
    whence = timezone.now() if whence is None else whence
    delta = datetime.timedelta(days=random.randint(1, 3999))
    return whence + delta

def sample_date_before(whence=None):
    whence = timezone.now() if whence is None else whence
    delta = datetime.timedelta(days=random.randint(-4000, 0))
    return whence + delta

def run():
    fake = Faker()

    cued_crsids = set('test{:04d}'.format(n) for n in range(1, 51))
    non_cued_crsids = set('test{:04d}'.format(n) for n in range(101, 151))

    # Sample non-cued users
    for crsid in cued_crsids.union(non_cued_crsids):
        m = sample_person(fake)

        u, _ = User.objects.get_or_create(username=crsid)
        u.email = '{}@example.com'.format(crsid)
        u.first_name = m['first_name']
        u.last_name = m['last_name']
        u.set_unusable_password()
        u.save()

        if crsid in cued_crsids:
            member, _ = Member.objects.get_or_create(
                user=u, is_active=random.random() < 0.75,
                arrived_on=sample_date_before())
            member.first_names = m['first_names']
            member.research_group = m['research_group']
            member.save()

            if random.random() < 0.1:
                n_statuses = 2
            else:
                n_statuses = 1

            for status in random.sample(STATUSES, n_statuses):
                end_on = sample_date_after(member.arrived_on)
                start_on = sample_date_before(member.arrived_on)
                Status.objects.create(
                    member=member, role=status, start_on=start_on,
                    end_on=end_on)

            if not member.is_active or random.random() < 0.1:
                member.last_inactive_on = sample_date_before()

    # Create superuser
    u = User.objects.get(username='test0001')
    m = Member.objects.get(user=u)
    m.is_active = True
    u.is_superuser = True
    u.is_staff = True
    m.save()
    u.save()

    # Create staff with no permissions
    u = User.objects.get(username='test0002')
    m = Member.objects.get(user=u)
    m.is_active = True
    u.is_staff = True
    m.save()
    u.save()

