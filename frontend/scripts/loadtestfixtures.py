"""
Load all test data into the database. (Useful for initialising a demo instance.)

"""
from django.core.management import call_command

# A list holding the fixtures to load
TEST_FIXTURES = [
    'cuedmembers/test_users_and_members',
    'mentoring/test_relationships',
]

def run():
    call_command('loaddata', *TEST_FIXTURES)
