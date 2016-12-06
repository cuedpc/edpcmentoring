from django.test import TestCase
#from edpcmentoring.models import User
from mentoring.models import Relationship, Meeting
from matching.models import Invitation, Preferences
from django.contrib.auth.models import User
from django.test.utils import setup_test_environment
from django.utils.timezone import now

# For our roles (not using these gone back to groups!!):
from rolepermissions.shortcuts import assign_role, remove_role
from rolepermissions.verifications import has_permission
from rolepermissions.shortcuts import grant_permission, revoke_permission

# To get the permissions set by models
from django.contrib.auth.models import Permission


import json

# Create your tests here.

from django.core.management import call_command

# A list holding the fixtures to load
TEST_FIXTURES = [
    'cuedmembers/test_users_and_members',
    'mentoring/test_relationships',
]




class CheckMatchMakerCase(TestCase):
    '''
    Check:
        endpoints are protected
        data can not be changed
        data is protected (users can only )
    '''

    #def test_login(self):
    def setUp(self):
        call_command('loaddata', *TEST_FIXTURES)
        setup_test_environment()
        users=[]
        users.append(User.objects.get(username='test0001'))
        users.append(User.objects.get(username='test0002'))
        users.append(User.objects.get(username='test0003'))
        for user in users:
            user.set_password('test')
            user.save()

        #set test0001 as a superuser
        t1 = User.objects.get(username='test0001')
        t1.is_superuser=True
        t1.save()


    def test_accesspage(self):
	#Test that  asuper user can do anything:
        t1 = User.objects.get(username='test0001')
        self.assertTrue(t1.has_perm('matching.matchmake'),"Super user can match")

        t3 = User.objects.get(username='test0003')
        self.assertFalse(t3.has_perm('matching.matchmake'),"user does not have permission to matchmake")

        #Test that without perms test0003 cannot access the matchmaker page :
        response = self.client.login(username='test0003', password='test')
        self.assertEqual(response,True)
	response = self.client.get('/matching',follow=True)
        self.assertEqual(response.status_code,403)

        t3.user_permissions.add(Permission.objects.get(codename='matchmake'))
        t3 = User.objects.get(username='test0003')
        #assign_role(t3, 'matchmake') # the django-role-permisisons way but how do we populate?
        self.assertTrue(t3.has_perm('matching.matchmake'),"user has permission to matchmake")
	# now t3 should be able to access '/matching
        response = self.client.get('/matching',follow=True)
        self.assertEqual(response.status_code,200)


