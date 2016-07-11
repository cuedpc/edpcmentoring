"""
I/O from and to the CUED members database.

"""
# Required to import the csv module correctly on Py 2.
from __future__ import absolute_import

import csv

from django.contrib.auth import get_user_model
from django.db import transaction

from . import get_member_group
from .models import Member, ResearchGroup, Division

# Field names in departmental CSV file.
_CSV_FIELD_NAMES = [
    'crsid', 'status', 'surname', 'fnames', 'pref_name', 'room', 'phone',
    'arrived', 'start_date', 'end_date', 'division', 'role_course',
    'host_supervisor', 'research_group'
]

def write_members_to_csv(csvfile, queryset):
    """
    Write the members returned in a queryset to a CSV file in the manner
    generated by the Department at:

        http://www-itsd.eng.cam.ac.uk/datadownloads/

    Fields not stored in the cuedmembers database are left blank.

    csvfile can be any object which supports a file-object-like write() method.

    """
    writer = csv.DictWriter(csvfile, _CSV_FIELD_NAMES)
    writer.writeheader()

    # Tell the query set which related fields we'll be using.
    related_queryset = queryset.select_related(
        'user', 'research_group', 'research_group__division'
    )

    for member in related_queryset:
        has_rg = member.research_group is not None
        division = member.research_group.division.letter if has_rg else None
        writer.writerow({
            'crsid': member.user.username,
            'surname': member.user.last_name,
            'fnames': member.first_names,
            'pref_name': member.user.first_name,
            'division': division,
            'research_group': member.research_group.name if has_rg else None,
        })

@transaction.atomic
def read_members_from_csv(csvfile, email_domain='cam.ac.uk'):
    """
    Read members into the database from a CSV file.

    Members not present in the CSV file but present in the database are marked
    as inactive. Members present in the CSV file but not in the database are
    created.

    csvfile can be any object supporting a file-object-like read() method.

    Will raise ResearchGroup.DoesNotExist if the CSV row has a non-empty
    research group name and division which does not correspond to one which
    exists in the database.

    """
    # Add rows from CSV file to database
    reader = csv.DictReader(csvfile)
    new_active_crsids = set()
    for row in reader:
        new_active_crsids.add(row['crsid'])
        research_group = row.get('research_group', '')
        if research_group != '':
            division = Division.objects.get(letter=row['division'])
            research_group, _ = ResearchGroup.objects.get_or_create(
                name=research_group, division=division)
        else:
            research_group = None

        Member.objects.update_or_create_by_crsid(
            row['crsid'], {
                'last_name': row.get('surname'),
                'first_name': row.get('pref_name'),
                'first_names': row.get('fnames'),
                'email': '{}@{}'.format(row['crsid'], email_domain),
                'research_group': research_group,
                'is_active': True,
            }
        )

    # Retrieve all active Member crsids from the database
    old_active_crs_ids = set(
        obj.user.username
        for obj in Member.objects.active().select_related('user')
    )

    # Mark departed members as inactive
    for crsid in old_active_crs_ids - new_active_crsids:
        m = Member.objects.get(user__username=crsid)
        m.is_active = False
        m.save()

    # Add active members to group, remove inactive ones
    member_group = get_member_group()
    user = get_user_model()
    member_group.user_set.add(*user.objects.filter(cued_member__is_active=True))
    member_group.user_set.remove(*user.objects.filter(
        cued_member__is_active=False))