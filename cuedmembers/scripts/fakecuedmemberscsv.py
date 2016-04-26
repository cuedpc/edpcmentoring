"""
Generate a CSV file full of fake CUED members. The CSV is written to standard
output.

The CSV should have a similar format to that documented at:

    http://www-itsd.eng.cam.ac.uk/datadownloads/support/div_people.html

"""
import csv
import sys

from cuedmembers.tests import fake_member_csv_rows

# Headings in departmental CSV file.
HEADINGS = [
    'crsid', 'status', 'surname', 'fnames', 'pref_name', 'room', 'phone',
    'arrived', 'start_date', 'end_date', 'div_id', 'role_course',
    'host_supervisor', 'rg_name'
]

def run():
    w = csv.DictWriter(sys.stdout, fieldnames=HEADINGS)
    w.writeheader()
    for crsid in ['test{:04d}'.format(x) for x in range(1, 100)]:
        w.writerows(fake_member_csv_rows(crsid))
