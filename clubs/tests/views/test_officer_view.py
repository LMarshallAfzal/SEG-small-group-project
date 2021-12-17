"""Test of the officer view"""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from clubs.forms import LogInForm
from clubs.models import User
from helpers import LogInTester
from django.contrib.auth.models import Group
from clubs.groups import Group
from clubs.club_list import ClubList

class OfficerViewTestCase(TestCase):
    """Tests of the officer view"""


    fixtures = [
        'clubs/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        list_of_clubs = ClubList()
        list_of_clubs.create_new_club("Cambridge Chessinators", "Cambridge > Oxford", "Cambridge")
        self.club = list_of_clubs.find_club("Cambridge Chessinators")
        self.url = reverse('officer')
        self.user = User.objects.get(username = 'johndoe@example.org')
        self.applicant = Group.objects.get(name=self.club.getClubApplicantGroup())
        self.member = Group.objects.get(name=self.club.getClubMemberGroup())
        self.officer = Group.objects.get(name=self.club.getClubOfficerGroup())
        self.client.login(email = self.user.email, Password = 'Password123')
        self.officer.user_set.add(self.user)


    def test_officer_url(self):
        self.assertEqual(self.url, '/officer/')

    
    def members_cannot_visit_officer(self):
        self.officer.user_set.remove(self.user)
        self.member.user_set.add(self.user)
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        response_url = reverse('profile')
        self.assertRedirects(response,response_url,status_code= 302, target_status_code= 200)
        self.assertTemplateUsed(response,'profile.html')

    def applicants_cannot_visit_officer(self):
        self.officer.user_set.remove(self.user)
        self.applicant.user_set.add(self.user)
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        response_url = reverse('profile')
        self.assertRedirects(response,response_url,status_code= 302, target_status_code= 200)
        self.assertTemplateUsed(response,'profile.html')

    def test_applicant_can_be_accepted(self):
        response = self.client.get(self.url)
        self.member.user_set.add(self.user)
        response_url = reverse('officer_promote_applicants')
        # self.assertRedirects(response, response_url, status_code = 302, target_status_code = 200)
        # self.assertTemplateUsed(response, 'officer_promote_applicants.html')
        # self.applicant.user_set.remove(self.user)
        self.assertFalse(self.user.groups.filter(name=self.club.getClubApplicantGroup()).exists())
        self.assertTrue(self.user.groups.filter(name=self.club.getClubMemberGroup()).exists())
        
    def test_applicant_can_be_rejected(self):
        before_count = User.objects.count()
        self.applicant.user_set.remove(self.user)
        self.assertFalse(self.user.groups.filter(name=self.club.getClubApplicantGroup()).exists())
        self.user.delete()
        after_count = User.objects.count()
        self.assertEqual(after_count,before_count-1)
        # response = self.client.post(self.url, self.user.id)
        # self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'officer_promote_applicants.html')



      
