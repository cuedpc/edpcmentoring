"""
The ``importcuedmembers`` management command is used to synchronise the
membership database with an authoritative source.

The Department provide CSV dumps of CUED membership. See
http://www-itsd.eng.cam.ac.uk/datadownloads/support/div_people.html
for more details. This command allows the ingestion of a CSV file in the format
outlined at that page into the database.

Members listed in the CSV file are created if they don't exist. Their personal
details, such as first name, surname, etc. are updated from the CSV. A
previously active member who does not appear in the CSV file is marked inactive.
Similarly, a previously inactive member who appears in the CSV file is marked
active.

By default, an email address of ``<crsid>@cam.ac.uk`` is used for each member.
This can be configured through the ``--email-domain`` argument.

This command can take either a path to a CSV file on the local system or a http
or https URL to a CSV file located on a remote server.

"""
# pylint: disable=wrong-import-order,import-error

from future.standard_library import install_aliases
install_aliases()

import sys
from urllib.parse import urlparse

from django.core.management.base import BaseCommand
from django.utils.six import StringIO
import requests

from ...csv import read_members_from_csv

class Command(BaseCommand):
    help = 'Dump active CUED members in CSV format'

    def add_arguments(self, parser):
        parser.add_argument(
            '-e', '--email-domain',
            metavar='DOMAIN', default='cam.ac.uk',
            help='Domain part of email addresses formed from CRSids')
        parser.add_argument(
            'csvfile', nargs='?', default=None,
            help='Path or URL to CSV file containing CUED membership')

    def handle(self, *args, **options):
        email_domain = options['email_domain']

        if options['csvfile'] is None:
            read_members_from_csv(sys.stdin, email_domain=email_domain)
        else:
            url_parts = urlparse(options['csvfile'])
            if url_parts.scheme == '':
                # File
                with open(options['csvfile']) as fobj:
                    read_members_from_csv(fobj, email_domain=email_domain)
            elif url_parts.scheme == 'http' or url_parts.scheme == 'https':
                # HTTP URL
                r = requests.get(options['csvfile'])
                r.raise_for_status()
                read_members_from_csv(
                    StringIO(r.content), email_domain=email_domain)
            else:
                raise ValueError(
                    'Unknown URL scheme: {}'.format(url_parts.scheme))
