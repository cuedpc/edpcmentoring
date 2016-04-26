import sys

from django.core.management.base import BaseCommand

from ...io import read_members_from_csv

class Command(BaseCommand):
    help = 'Dump active CUED members in CSV format'

    def add_arguments(self, parser):
        parser.add_argument(
            '-e', '--email-domain',
            metavar='DOMAIN', default='cam.ac.uk',
            help='Domain part of email addresses formed from CRSids')
        parser.add_argument(
            'csvfile', nargs='?', default=None,
            help='CSV file containing CUED membership')

    def handle(self, *args, **options):
        email_domain = options['email_domain']
        if options['csvfile'] is None:
            read_members_from_csv(sys.stdin, email_domain=email_domain)
        else:
            with open(options['csvfile']) as fobj:
                read_members_from_csv(fobj, email_domain=email_domain)
