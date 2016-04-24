import csv

from django.core.management.base import BaseCommand

from cuedmembers.models import Member

FIELDS = [
    ('CRSid', lambda o: o.user.username),
    ('Full name', lambda o: o.user.get_full_name()),
    ('Division', lambda o: o.division),
    ('Arrival date',
     lambda o: o.arrived_on.isoformat() if o.arrived_on is not None else ''),
    ('Expected departure date',
     lambda o: o.expected_departure_on.isoformat() if o.expected_departure_on is not None else ''),
]

class Command(BaseCommand):
    help = 'Dump active CUED members in CSV format'

    def add_arguments(self, parser):
        parser.add_argument('-o', '--output',
                            metavar='FILE', type=str,
                            help='File to save output to')

    def handle(self, *args, **options):
        if options['output'] is None:
            self.dump_active_members(self.stdout)
        else:
            with open(options['output'], 'w') as fobj:
                self.dump_active_members(fobj)

    def dump_active_members(self, file_object):
        writer = csv.writer(file_object)
        writer.writerow([k for k, _ in FIELDS])
        for o in Member.objects.active():
            writer.writerow([cb(o) for _, cb in FIELDS])
