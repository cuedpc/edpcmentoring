# pylint: disable=wrong-import-order,import-error

from future.standard_library import install_aliases
install_aliases()

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
import sys
from urllib.parse import urlparse

from django.core.management.base import BaseCommand
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
