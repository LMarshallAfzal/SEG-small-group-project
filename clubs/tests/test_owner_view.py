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
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_user.json'
    ]
    

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.url = reverse('owner')

        owner = Group.objects.get(name = "Owner")
        owner.user_set.add(self.user)

        officer = Group.objects.get(name = "Officer")
        other_user = User.objects.get(username = 'janedoe@example.org')
        officer.user_set.add(other_user)

        member = Group.objects.get(name = "Member")
        member_user = User.objects.get(username = "petrapickles@example.org")
        member.user_set.add(member_user)



        applicant = Group.objects.get(name = "Applicant")
        applicant_user = User.objects.get(username = "peterpickles@example.org")
        applicant.user_set.add(member_user)


        other_user_officer = self.assertIn(self.officer,self.other_user)
        

    def test_owner_url(self):
        self.assertEqual(self.url,'/owner/')

    
    
    def test_promote_member(self):
        pass
        

    
    def test_can_only_promote_officer_to_owner(self):
        self.officer.user_set.remove(self.other_user)
        self.assertFalse(self.other_user_officer)
        self.owner.user_set.add(self.other_user)
        self.assertNotIn(self.owner,self.other_user)

    
    def test_officer_can_be_promoted(self):
        self.assertTrue(self.other_user_officer)
        self.owner.user_set.add(self.other_user)
        self.assertIn(self.owner,self.other_user)


    def test_owner_change(self):
        owners = self.owner.user_set.getAll.toList
        current_owner = owners[0]
        self.owner.user_set.add(self.other_user)
        self.owner.user_set.remove(current_owner)
        owner_count = self.owner.user_set.count
        self.assertEqual(owner_count,1)
        owners = self.owner.user_set.getAll.toList
        current_owner = owners[0]
        self.assertEqual(owners[0],self.other_user)
    
    
        
        
        
        