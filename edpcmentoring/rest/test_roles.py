from django.test import TestCase
#from edpcmentoring.models import User
from mentoring.models import Relationship, Meeting
from matching.models import Invitation, Preferences
from django.contrib.auth.models import User, Group, Permission
from django.test.utils import setup_test_environment
from django.utils.timezone import now

from django.shortcuts import get_object_or_404

# For our roles:
from rolepermissions.shortcuts import assign_role, remove_role
from rolepermissions.verifications import has_permission
from rolepermissions.shortcuts import grant_permission, revoke_permission


import json

# Create your tests here.

from django.core.management import call_command

# A list holding the fixtures to load
TEST_FIXTURES = [
    'cuedmembers/test_users_and_members',
    'mentoring/test_relationships',
    'rest/edpcmentoring_perms',
]




class CheckMatchMakerAccessCase(TestCase):
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
        users.append(User.objects.get(username='test0003'))
        for user in users:
            user.set_password('test')
            user.save()

        #set test0001 as a superuser
        t1 = User.objects.get(username='test0001')
        t1.is_superuser=True
        t1.save()


    def test_matchmaker(self):

        matchmakers = Group.objects.get(name='matchmakers')
 
        #Test non-matchmaker is denied access:
        response = self.client.login(username='test0003', password='test')
        self.assertEqual(response,True)
        response = self.client.get('/api/mm/seekrel/?mentee=true')
        self.assertEqual(response.status_code,403);
        response = self.client.get('/api/mm/seekrel/?mentor=true')
        self.assertEqual(response.status_code,403);


        #Test that  asuper user can do anything:
        t1 = User.objects.get(username='test0001')
        self.assertTrue(t1.has_perm('matching.matchmake'),"Super user can matchmake")

        t3 = User.objects.get(username='test0003')
        self.assertFalse(t3.has_perm('matching.matchmake'),"user does not have permission to add matchmake")
        t3.groups.add(matchmakers)
        perm = Permission.objects.get(codename='matchmake')
        print perm
        t3.user_permissions.add(perm)
        
        #t3 = get_object_or_404(User, pk=t3.id)

        t3 = User.objects.get(username='test0003')
        self.assertTrue(t3.has_perm('matching.matchmake'),"user has permission to matchmake")

        #Also test that the matchmakers can see the same info:
        response = self.client.login(username='test0003', password='test')
        self.assertEqual(response,True)

        response = self.client.get('/api/mm/seekrel/?mentee=true')
        self.assertEqual(response.status_code,200);
        response = self.client.get('/api/mm/seekrel/?mentor=true')
        self.assertEqual(response.status_code,200);

        t3.groups.remove(matchmakers) #removes matchmaker perms
        self.assertFalse(t3.has_perm('matching.matchemake'),"user no longer has permission to matchmake")

        #test that after removing the group the user can no longer access the pages:
#  not working - subtlety in perms cache
#        response = self.client.login(username='test0003', password='test')
#        self.assertEqual(response,True)
#        response = self.client.get('/api/mm/seekrel/?mentee=true')
#        self.assertEqual(response.status_code,403);
#        response = self.client.get('/api/mm/seekrel/?mentor=true')
#        self.assertEqual(response.status_code,403);


       

        # test unauth user can not log in
#        response = self.client.get('/',follow=True)
#        self.assertEqual(response.status_code, 404)

        # test regular user can not see others invitations
        # log in user:
#        response = self.client.login(username='test0001', password='test')
#        self.assertEqual(response,True)

        # attempt to view user/2 should be denied
