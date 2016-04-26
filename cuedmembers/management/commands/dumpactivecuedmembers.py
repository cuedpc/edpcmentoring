from django.core.management.base import BaseCommand

from cuedmembers.io import write_members_to_csv
from cuedmembers.models import Member

class Command(BaseCommand):
    help = 'Dump active CUED members in CSV format'

    def add_arguments(self, parser):
        parser.add_argument('-o', '--output',
                            metavar='FILE', type=str,
                            help='File to save output to')

    def handle(self, *args, **options):
        qs = Member.objects.active().order_by('user__username')
        if options['output'] is None:
            write_members_to_csv(self.stdout, qs)
        else:
            with open(options['output'], 'w') as fobj:
                write_members_to_csv(fobj, qs)
