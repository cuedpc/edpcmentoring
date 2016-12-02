from django.test import TestCase
#from edpcmentoring.models import User
from mentoring.models import Relationship, Meeting
from matching.models import Invitation, Preferences
from django.contrib.auth.models import User
from django.test.utils import setup_test_environment
from django.utils.timezone import now

import json

# Create your tests here.

from django.core.management import call_command

# A list holding the fixtures to load
TEST_FIXTURES = [
    'cuedmembers/test_users_and_members',
    'mentoring/test_relationships',
]

#def run():
#    call_command('loaddata', *TEST_FIXTURES)



class CheckDenyAccessCase(TestCase):
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
        users.append(User.objects.get(username='test0004'))
        users.append(User.objects.get(username='test0005'))
        users.append(User.objects.get(username='test0006'))
        users.append(User.objects.get(username='test0007'))
        users.append(User.objects.get(username='test0008'))
        users.append(User.objects.get(username='test0009'))
        users.append(User.objects.get(username='test0010'))
        users.append(User.objects.get(username='test0011'))
        users.append(User.objects.get(username='test0012'))
        for user in users:
            user.set_password('test')
            user.save()

        #set test0001 as a superuser
        t1 = User.objects.get(username='test0001')
        t1.is_superuser=True
        t1.save()

    def test_api_users(self):
        # test unauth user can not log in
        response = self.client.get('/',follow=True)
        self.assertEqual(response.status_code, 404)

        # test regular user can not see others invitations
        # log in user:
        response = self.client.login(username='test0001', password='test')
        self.assertEqual(response,True)

        # attempt to view user/2 should be denied
        res = self.client.get('/api/users/2',follow=True)
        self.assertEqual(res.status_code, 403)

        # attempt to view own details should be fine
        res = self.client.get('/api/users/1',follow=True)
        self.assertEqual(res.status_code, 200)

    def test_api_current(self):

        # log in user:
        response = self.client.login(username='test0001', password='test')
        self.assertEqual(response,True)

        # attempt to view user/2 should be denied    
        res = self.client.get('/api/current',follow=True)
        self.assertEqual(res.status_code, 200)
        myj = json.loads(res.content.decode('utf-8'))
        self.assertEqual(myj[0][u'username'],'test0001',"logged in as user test0001")


    def test_api_preferences(self):
        
        # log in user:
        response = self.client.login(username='test0001', password='test')
        self.assertEqual(response,True)

        # attempt to view user/2 should be denied
        res = self.client.get('/api/current_preferences',follow=True)
        self.assertEqual(res.status_code, 200)


    def test_api_proxy(self):
        
        #deny - not sure what this is used for atm
        #     - implement as part of management interface
        
        response = self.client.login(username='test0001', password='test')
        self.assertEqual(response,True)

        res = self.client.get('/api/proxy',follow=True)
        self.assertEqual(res.status_code, 404)


    def test_api_groups(self):
        #deny - again to implement as part of the manager interface
        #     - when implemented make sure only managers can view
        
        response = self.client.login(username='test0001', password='test')
        self.assertEqual(response,True)

        res = self.client.get('/api/proxy',follow=True)
        self.assertEqual(res.status_code, 404)


    def test_api_basicrel(self):
        # only allow mentor, mentee and manager ability to put / get /post
        

        # create a relationship test0010 - test0011, mentee - mentor
        rel = Relationship.objects.create(mentor=User.objects.get(username='test0010'),mentee=User.objects.get(username='test0011'),is_active=True)
        # what is the id of the relationship we have?

        #TODO use regular user (test0005 hopefully!) to test that they can not access the relatiomship 
        # log in user:
        response = self.client.login(username='test0005', password='test')
        self.assertEqual(response,True)

        # attempt to view user/2 should be denied
        res = self.client.get('/api/basicrel/'+str(rel.id),follow=True)
        self.assertEqual(res.status_code, 403, "deny access for non mentor mentee (and manager - TODO)")

        # check that both 10 and 11 can view it (TODO check manager)

        response = self.client.login(username='test0010', password='test')
        self.assertEqual(response,True,"test0010 logged in")

        # attempt to view relationshio should be accepted
        res = self.client.get('/api/basicrel/'+str(rel.id),follow=True)
        self.assertEqual(res.status_code, 200, "deny access for non mentor mentee (and manager - TODO)")

            
        response = self.client.login(username='test0011', password='test')
        self.assertEqual(response,True,"test0011 logged in")

        # attempt to view relationshio should be accepted
        res = self.client.get('/api/basicrel/'+str(rel.id),follow=True)
        self.assertEqual(res.status_code, 200, "deny access for non mentor mentee (and manager - TODO)")

        #super user        
        response = self.client.login(username='test0001', password='test')
        self.assertEqual(response,True,"test0001 logged in")

        # attempt to view relationshio should be accepted
        res = self.client.get('/api/basicrel/'+str(rel.id),follow=True)
        self.assertEqual(res.status_code, 200, "deny access for non mentor mentee (and manager - TODO)")


    def test_api_meetings(self):
        # only allow mentor, mentee and manager ability to post a new meeting

        response = self.client.login(username='test0007', password='test')
        self.assertEqual(response,True,"test0007 logged in")

        rel = Relationship.objects.create(mentor=User.objects.get(username='test0010'),mentee=User.objects.get(username='test0011'),is_active=True)
    
        res = self.client.post('/api/meetings/',{'approximate_duration':40,'held_on':now().date(),'relationship':'/api/basicrel/'+str(rel.id)+'/'})
        # 400 invalid data (post)
        self.assertEqual(res.status_code, 400, "deny creation of meeting where user not superuser and not mentor/mentee")
        

        # A super user should be able to register a meeting
        response = self.client.login(username='test0001', password='test')
        self.assertEqual(response,True,"test0001 (superuser) logged in")

        res = self.client.post('/api/meetings/',{'approximate_duration':40,'held_on':now().date(),'relationship':'/api/basicrel/'+str(rel.id)+'/'})
        # 201 -> created
        self.assertEqual(res.status_code, 201, "allow creation of meeting where user is superuser and not mentor/mentee")
        myj = json.loads(res.content.decode('utf-8'))
        mtg = Meeting.objects.get(id=myj['id'])
        self.assertEqual(str(mtg.get_mentor()),'test0010')
        self.assertEqual(str(mtg.get_mentee()),'test0011')
 
        # The Mentor should be able to register a meeting
        response = self.client.login(username='test0010', password='test')
        self.assertEqual(response,True,"test0010 (mentor) logged in")

        res = self.client.post('/api/meetings/',{'approximate_duration':40,'held_on':now().date(),'relationship':'/api/basicrel/'+str(rel.id)+'/'})
        # 201 -> created
        self.assertEqual(res.status_code, 201, "allow creation of meeting where user is superuser and not mentor/mentee")


        # The Mentee should be able to register a meeting
        response = self.client.login(username='test0011', password='test')
        self.assertEqual(response,True,"test0011 (mentor) logged in")

        res = self.client.post('/api/meetings/',{'approximate_duration':40,'held_on':now().date(),'relationship':'/api/basicrel/'+str(rel.id)+'/'})
        # 201 -> created
        self.assertEqual(res.status_code, 201, "allow creation of meeting where user is superuser and not mentor/mentee")


    def test_api_invitations(self):
        ''' 
        test that only superuser, and mentor and mentee can accept and decline
        '''

        # only allow mentor, mentee and manager ability to post a new meeting

        inv = Invitation.objects.create(mentor=User.objects.get(username='test0010'),mentee=User.objects.get(username='test0011'),created_by=User.objects.get(username='test0011'))

        response = self.client.login(username='test0007', password='test')
        self.assertEqual(response,True,"test0007 logged in")

        res = self.client.put('/api/invitations/'+str(inv.id)+'/',{'mentor_response':'"A"'},'application/json')
        # 400 invalid data (post)
        self.assertEqual(res.status_code, 400, "deny update of invitation where user not superuser and not mentor/mentee")
    
        response = self.client.login(username='test0001', password='test')
        self.assertEqual(response,True,"test0001 (superuser) logged in")
# TODO allow at model level!
#                res = self.client.put('/api/invitations/'+str(inv.id)+'/',json.dumps({'mentor_response':'A')},'application/json')
#        #print "can we provide the relation via id? rather than full on model? or url? "+res
#                # 204 updated 
#        print res.status_code
#        self.assertEqual(res.status_code, 204, "allow update of invitation where user is superuser")
            
        response = self.client.login(username='test0010', password='test')
        self.assertEqual(response,True,"test0010 (mentor) logged in")

        res = self.client.put('/api/invitations/'+str(inv.id)+'/',json.dumps({'mentor_response':'A'}),'application/json')
        # 200 updated 
        self.assertEqual(res.status_code, 200, "allow update of invitation where user mentor updating mentor_response")
    
        response = self.client.login(username='test0011', password='test')
        self.assertEqual(response,True,"test0011 (mentee) logged in")

        res = self.client.put('/api/invitations/'+str(inv.id)+'/',json.dumps({'mentor_response':'A'}),'application/json')
        # 400 updated 
        self.assertEqual(res.status_code, 400, "deny update of invitation where mentee updating mentor acceptance")
    
        res = self.client.put('/api/invitations/'+str(inv.id)+'/',json.dumps({'mentee_response':'A'}),'application/json')
        # 200 updated 
        self.assertEqual(res.status_code, 200, "allow update of invitation where mentee updating mentee acceptance")


    
    def test_api_myinvitations(self):
        '''
        My invitations accessible by get only
        '''
        response = self.client.login(username='test0010', password='test')
        self.assertEqual(response,True,"test0010 (mentor) logged in")

        #MyInvitations are read only
        res = self.client.options('/api/myinvitations/')
        self.assertEqual(str(res['Allow']),"GET, OPTIONS")



class testInvitations(TestCase):
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
        users.append(User.objects.get(username='test0004'))
        users.append(User.objects.get(username='test0005'))
        users.append(User.objects.get(username='test0006'))
        users.append(User.objects.get(username='test0007'))
        users.append(User.objects.get(username='test0008'))
        users.append(User.objects.get(username='test0009'))
        users.append(User.objects.get(username='test0010'))
        users.append(User.objects.get(username='test0011'))
        users.append(User.objects.get(username='test0012'))
        for user in users:
            user.set_password('test')
            user.save()

        #set test0001 as a superuser
        t1 = User.objects.get(username='test0001')
        t1.is_superuser=True
        t1.save()

        #test0002 is accepting mentees
        Preferences.objects.create(user=User.objects.get(username='test0002'),is_seeking_mentee=True,is_seeking_mentor=False)

        #test0003 is looking for a mentor
        Preferences.objects.create(user=User.objects.get(username='test0003'),is_seeking_mentee=False,is_seeking_mentor=True)

        #test0004 is not acepting mentees or looking for a mentor
        Preferences.objects.create(user=User.objects.get(username='test0004'),is_seeking_mentee=False,is_seeking_mentor=False)

        

    def test_invite_mentee(self):

        #test that if we are NOT accepting mentees we can not send the invite
        response = self.client.login(username='test0004', password='test')
        self.assertEqual(response,True)

        #get base url for the test server (which might always be http://testsever!
        response = self.client.get('/api/current/')
        myj = json.loads(response.content.decode('utf-8'))
        base = "/".join(myj[0]['url'].split('/')[:-4])
        #print "base: "+base
  
        #test0004 should be able to see both test0003 and test0002 searching for a Mentor, Mentee respectively
	
        response = self.client.get('/api/seekrel/?mentee=true')
        myj = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(myj),1);
	
        response = self.client.get('/api/seekrel/?mentor=true')
        myj = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(myj),1);


        # try someone looking for a mentor:
        searching = base+'/api/users/'+str(User.objects.get(username='test0003').id)+'/'
        #print searching 
        response = self.client.post('/api/invitations/',{'mentee':searching})
        #print str(response)        
        self.assertEqual(response.status_code, 400)
        
        #Try someone who is not looking for a mentor:
        searching = User.objects.get(username='test0002')
        response = self.client.post('/api/invitations/',{'mentee':base+'/api/users/'+str(searching.id)+'/'})
        self.assertEqual(response.status_code, 400)
        #print "response:"+ response        

        # LOGIN as a user looking for a Mentee! 
        #Test that if we are accepting mentees we can not send the invite to a user not looking for a mentor
        response = self.client.login(username='test0002', password='test')
        self.assertEqual(response,True)
        # try someone looking for a mentor:
        searching = User.objects.get(username='test0004')
        response = self.client.post('/api/invitations/',{'mentee':base+'/api/users/'+str(searching.id)+'/'})
        #print "response: "+str(response)
        self.assertEqual(response.status_code, 400)
                
       
        #Test that if we are accepting mentees we can send the invite to a user looking for a mentor
        #Try someone who is looking for a mentor:
        searching = User.objects.get(username='test0003')
        response = self.client.post('/api/invitations/',{'mentee':base+'/api/users/'+str(searching.id)+'/'})
        #print "response: "+str(response)
        self.assertEqual(response.status_code, 201)

    def test_accept_decline_invite(self):
        # send invitation to seeker        
 
        # LOGIN as a user looking for a Mentee! 
        #Test that if we are accepting mentees we can not send the invite to a user not looking for a mentor
        response = self.client.login(username='test0002', password='test')
        self.assertEqual(response,True)
       
        #get base url for the test server (which might always be http://testsever!
        response = self.client.get('/api/current/')
        myj = json.loads(response.content.decode('utf-8'))
        base = "/".join(myj[0]['url'].split('/')[:-4])
        #print "base: "+base


        #Test that if we are accepting mentees we can send the invite to a user looking for a mentor
        #Try someone who is looking for a mentor:
        searching = User.objects.get(username='test0003')
        response = self.client.post('/api/invitations/',{'mentee':base+'/api/users/'+str(searching.id)+'/'})
        #print "response: "+str(response)
        self.assertEqual(response.status_code, 201)

        #test0003 will accept:
        response = self.client.login(username='test0003', password='test')
        self.assertEqual(response,True)
        response = self.client.get("/api/myinvitations/")
        self.assertEqual(response.status_code, 200)
        invid = json.loads(response.content.decode('utf-8'))[0]['id']
        self.client.put("/api/invitations/"+str(invid)+"/",json.dumps({'mentee_response':'A'}),'application/json')
        self.assertEqual(response.status_code, 200)
        #print str(response)
        
        #Above should generate a relationship check relationship exists for both parties
        response = self.client.login(username='test0002', password='test')
        self.assertEqual(response,True)
        response = self.client.get("/api/mentees/")
        self.assertEquals(len(json.loads(response.content.decode('utf-8'))),1)

        response = self.client.login(username='test0003', password='test')
        self.assertEqual(response,True)
        #print "There should be a relationship in here!!!"        
        response = self.client.get("/api/mentors/")
        #print str(response)
        rel = json.loads(response.content.decode('utf-8'))[0]

        myrel = Relationship.objects.get(id=rel['id'])
        self.assertEqual(str(myrel),'test0002 mentoring test0003',"the relationship "+str(myrel)+" is active")

        rel['is_active']=False
        response = self.client.put("/api/basicrel/"+str(rel['id'])+"/",json.dumps(rel),'application/json')
        self.assertEqual(response.status_code, 200)
        
        #Test that the database object has an ended on date
        myrel = Relationship.objects.get(id=rel['id'])
        self.assertTrue(myrel.ended_on)
        self.assertTrue(myrel.ended_by)


class testUser(TestCase):
    '''
    Check:
        User can update their privileges
        # can not update others - unless superuser (or roles have been defined)
        # 
    '''

    #def test_login(self):
    def setUp(self):
        call_command('loaddata', *TEST_FIXTURES)
        setup_test_environment()
        users=[]
        users.append(User.objects.get(username='test0001'))
        users.append(User.objects.get(username='test0002'))
        users.append(User.objects.get(username='test0003'))
        users.append(User.objects.get(username='test0004'))
        for user in users:
            user.set_password('test')
            user.save()

        #set test0001 as a superuser
        t1 = User.objects.get(username='test0001')
        t1.is_superuser=True
        t1.save()

        #test0002 is accepting mentees
        Preferences.objects.create(user=User.objects.get(username='test0002'),is_seeking_mentee=False,is_seeking_mentor=False)




    def test_update_prefs(self):
        # LOGIN as a user looking for a Mentee! 
        #Test that if we are accepting mentees we can not send the invite to a user not looking for a mentor
        response = self.client.login(username='test0002', password='test')
        self.assertEqual(response,True)
        # try someone looking for a mentor:
        response = self.client.get('/api/current/')
        self.assertEqual(response.status_code, 200)
        me = json.loads(response.content.decode('utf-8'))[0]
        self.assertEqual(me['mentorship_preferences']['is_seeking_mentor'],False)
        self.assertEqual(me['mentorship_preferences']['is_seeking_mentee'],False)
               
        me['mentorship_preferences']['is_seeking_mentor']=True
        response = self.client.put('/api/users/'+str(me['id'])+'/',json.dumps(me),'application/json')
        self.assertEqual(response.status_code,200)

        response = self.client.get('/api/current/')
        self.assertEqual(response.status_code, 200)
        me = json.loads(response.content.decode('utf-8'))[0]
        self.assertEqual(me['mentorship_preferences']['is_seeking_mentor'],True)
        self.assertEqual(me['mentorship_preferences']['is_seeking_mentee'],False)
         
        me['mentorship_preferences']['is_seeking_mentee']=True
        response = self.client.put('/api/users/'+str(me['id'])+'/',json.dumps(me),'application/json')
        self.assertEqual(response.status_code,200)

        response = self.client.get('/api/current/')
        self.assertEqual(response.status_code, 200)
        me = json.loads(response.content.decode('utf-8'))[0]
        self.assertEqual(me['mentorship_preferences']['is_seeking_mentor'],True)
        self.assertEqual(me['mentorship_preferences']['is_seeking_mentee'],True)
        
