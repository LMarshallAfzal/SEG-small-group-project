"""Test of the officer view"""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from clubs.models import User
from django.contrib.auth.models import Group

class UserFormTestCase(TestCase):
    """Unit tests of the user form."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_user.json',
        'clubs/tests/fixtures/member.json',
        'clubs/tests/fixtures/applicant.json',
    ]
    

    def setUp(self):
        self.user = User.objects.get(email = "johndoe@example.org")
        self.url = reverse('owner')
        self.officer_user = User.objects.get(email = 'janedoe@example.org')
        self.member_user = User.objects.get(email = 'petrapickles@example.org')
        self.applicant_user = User.objects.get(email = 'peterpickles@example.org')

        owner = Group.objects.get(name = "Owner")
        owner.user_set.add(self.user)

        officer = Group.objects.get(name = "Officer")
        officer.user_set.add(self.officer_user)

        member = Group.objects.get(name = "Member")
        member.user_set.add(self.member_user)

        applicant = Group.objects.get(name = "Applicant")
        applicant.user_set.add(self.applicant_user)



        
        

    def test_owner_url(self):
        self.assertEqual(self.url,'/owner/')

    def test_get_owner(self):
        response = self.client.url
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('owner.html')

    def test_promote_member_to_officer(self):
        self.assertFalse(self.member_user.groups.filter(name='Officer').exists())
        self.assertTrue(self.member_user.groups.filter(name='Member').exists())
        self.officer.user_set.add(self.member_user)
        self.member.user_set.remove(self.member_user)
        self.assertTrue(self.member_user.groups.filter(name='Officer').exists())  
        self.assertFalse(self.member_user.groups.filter(name='Member').exists())
        response = self.client.post(self.url,self.officer_user.id,follow=True)
        response_url = reverse('officer_list')
        self.assertRedirects(response,response_url,status_code= 302, target_status_code= 200)
        self.assertTemplateUsed(response,'officer_list.html')

    def test_officer_can_be_demoted(self):
        self.assertTrue(self.officer_user.groups.filter(name='Officer').exists())
        self.officer.user_set.remove(self.officer_user)
        self.member.user_set.add(self.officer_user)
        self.assertFalse(self.officer_user.groups.filter(name='Officer').exists())
        self.assertTrue(self.officer_user.groups.filter(name='Member').exists())
        response = self.client.post(self.url,self.officer_user.id,follow=True)
        response_url = reverse('officer_list')
        self.assertRedirects(response,response_url,status_code= 302, target_status_code= 200)
        self.assertTemplateUsed(response,'officer_list.html')

    
    def test_cannnot_promote_member_to_owner(self):
        self.assertFalse(self.member_user.groups.filter(name='Officer').exists())
        self.assertTrue(self.member_user.groups.filter(name='Member').exists())
        self.owner.user_set.add(self.member_user)
        self.assertFalse(self.member_user.groups.filter(name='Owner').exists())  
        self.assertFalse(self.member_user.groups.filter(name='Officer').exists())  
        response = self.client.post(self.url,self.other_user.id,follow=True)
        response_url = reverse('owner_member_list')
        self.assertRedirects(response,response_url,status_code= 302, target_status_code= 200)
        self.assertTemplateUsed(response,'owner_member_list.html')


    def test_cannnot_promote_applicant_to_owner(self):
        self.assertFalse(self.applicant_user.groups.filter(name='Officer').exists())
        self.assertFalse(self.applicant_user.groups.filter(name='Member').exists())
        self.assertTrue(self.applicant_user.groups.filter(name='Applicant').exists())
        self.owner.user_set.add(self.applicant_user)
        self.assertFalse(self.applicant_user.groups.filter(name='Owner').exists()) 
        self.assertFalse(self.applicant_user.groups.filter(name='Officer').exists())  
        self.assertFalse(self.applicant_user.groups.filter(name='Member').exists())   
        response = self.client.post(self.url,self.other_user.id,follow=True)
        response_url = reverse('owner_member_list')
        self.assertRedirects(response,response_url,status_code= 302, target_status_code= 200)
        self.assertTemplateUsed(response,'owner_member_list.html')

    
    def test_officer_can_be_promoted(self):
        self.assertTrue(self.other_user_officer)
        self.owner.user_set.add(self.other_user)
        self.assertTrue(self.user.groups.filter(name='Owner').exists())


    def test_owner_change(self):
        response = self.client.post(self.url,self.other_user.id,follow=True)
        response_url = reverse('log_in')
        self.assertRedirects(response,response_url,status_code= 302, target_status_code= 200)
        self.assertTemplateUsed('log_in.html')
        owners = self.owner.user_set.getAll.toList
        current_owner = owners[0]
        self.owner.user_set.add(self.other_user)
        self.owner.user_set.remove(current_owner)
        owner_count = len((self.owner.user_set.all()).toList)
        self.assertEqual(owner_count,1)
        owners = self.owner.user_set.getAll.toList
        current_owner = owners[0]
        self.assertEqual(owners[0],self.other_user)
    
    
        
        
        
        