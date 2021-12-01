"""Test of the officer view"""
from unittest.loader import defaultTestLoader
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from clubs.forms import LogInForm
from clubs.models import User
from clubs.views import officer
from .helpers import LogInTester
from django.contrib.auth.models import Group

class UserFormTestCase(TestCase):
    """Unit tests of the user form."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json'
        'clubs/tests/fixtures/other_user.json'
    ]
    

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.url = reverse('owner')
        self.other_user = User.objects.get(username = 'janedoe@example.org')

        member = Group.objects.get(name = "Member")
        member.user_set.add(self.user)
        member.user_set.add(self.other_user)

        officer = Group.objects.get(name = "Officer")
        member.user_set.add(self.user)
        officer.user_set.add(self.other_user)

        owner = Group.objects.get(name = "Owner")
        member.user_set.add(self.user)
        owner.user_set.add(self.user)


        
        

    def test_owner_url(self):
        self.assertEqual(self.url,'/owner/')

    def test_get_owner(self):
        response = self.client.url
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('owner.html')

    
    """inherit from officer test"""
    def test_promote_member(self):
            pass
        

    
    def test_can_only_promote_officer_to_owner(self):
        self.officer.user_set.remove(self.other_user)
        self.assertFalse(self.other_user.groups.filter(name='Officer').exists())
        self.owner.user_set.add(self.other_user)
        self.assertFalse(self.other_user.groups.filter(name='Owner').exists())  
        response = self.client.post(self.url,self.other_user.id)
        response_url = reverse('member_list')
        self.assertRedirects(response,response_url,status_code= 302, target_status_code= 200)
        self.assertTemplateUsed(response,'member_list.html')

    
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
    
    
        
        
        
        