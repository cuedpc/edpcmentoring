import datetime
import random

from django.utils import timezone
from faker import Faker

from ..models import ResearchGroup

STATUSES = ['staff', 'pgrad', 'visitor']

def _sample_date_after(whence=None):
    whence = timezone.now().date() if whence is None else whence
    delta = datetime.timedelta(days=random.randint(1, 3999))
    return whence + delta

def _sample_date_before(whence=None):
    whence = timezone.now().date() if whence is None else whence
    delta = datetime.timedelta(days=random.randint(-4000, 0))
    return whence + delta

def member_csv_rows(crsid):
    """
    Generate a sequence of rows corresponding to rows in the Department CSV data
    dumps documented at:

    http://www-itsd.eng.cam.ac.uk/datadownloads/support/div_people.html

    But with the field names corrected to correspond to the actual CSV :).

    The rows all correspond to the same user identified by the CRSid passed. The
    names are chosen without reference to the letters in the CRSid. Since a CUED
    member may have multiple statuses, this function may return multiple rows.
    These rows differ only in the "Status", "Start date" and "End date" fields.

    Return a dictionary mapping column name to value. Missing values may not
    appear in the returned dictionary.

    The "Host/supervisor", "Room" and "Phone" columns are always missing.

    This function requires that the ResearchGroup and Division models have data.

    """
    # pylint:disable=too-many-locals

    fake = Faker()

    # For the sake of database testing, gender is binary when it comes to
    # generating names and prefixes.
    if random.random() < 0.5:
        make_first_name = fake.first_name_female
        make_prefix = fake.prefix_female
    else:
        make_first_name = fake.first_name_male
        make_prefix = fake.prefix_male

    base_row = {'crsid': crsid}

    first_name_list = [make_first_name() for _ in range(random.randint(1, 3))]
    prefix = make_prefix()
    base_row['pref_name'] = random.choice(first_name_list)
    base_row['fnames'] = ' '.join(first_name_list)
    base_row['surname'] = fake.last_name()

    arrived = random.random() > 0.2
    base_row['arrived'] = 'Yes' if arrived else 'No'

    # Simulate a small number of people having no research group
    if random.random() > 0.1:
        research_group = random.choice(ResearchGroup.objects.all())
        base_row['division'] = research_group.division.letter
        base_row['research_group'] = research_group.name

    # A small number of people have multiple statuses
    status_count = 1 if (random.random() > 0.2) else 2
    statuses = random.sample(STATUSES, status_count)

    rows = []
    for status in statuses:
        row = {}
        row.update(base_row)
        row['status'] = status
        arrived_on = _sample_date_before()
        end_on = _sample_date_after(arrived_on)
        start_on = _sample_date_before(arrived_on)
        row['start_date'] = start_on.strftime('%d-%b-%Y').upper()
        row['end_date'] = end_on.strftime('%d-%b-%Y').upper()
        rows.append(row)

    return rows


