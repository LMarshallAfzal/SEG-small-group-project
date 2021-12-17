"""Test of the officer view"""
from selenium.webdriver.chrome.webdriver import WebDriver
import time
from django.urls import reverse
from clubs.models import User, Club
from django.contrib.auth.models import Group
from clubs.club_list import ClubList
from django.test import TestCase

#TestCase, LiveServerTestCase):

class OwnerViewTestCase(TestCase):
    """Unit tests of the user form."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_user.json',
        'clubs/tests/fixtures/member.json',
        'clubs/tests/fixtures/applicant.json',
    ]

#To do fix tests
    def setUp(self):
        list_of_clubs = ClubList()
        list_of_clubs.create_new_club("Cambridge Chessinators", "Cambridge > Oxford", "Cambridge")
        self.club = list_of_clubs.find_club('Cambridge Chessinators')
        self.url = reverse('owner')
        self.officer_user = User.objects.get(username = 'janedoe@example.org')
        self.user = User.objects.get(username = 'johndoe@example.org')
        self.member_user = User.objects.get(username = 'petrapickles@example.org')
        self.applicant_user = User.objects.get(username = 'peterpickles@example.org')
        self.applicant = Group.objects.get(name=self.club.getClubApplicantGroup())
        self.member = Group.objects.get(name=self.club.getClubMemberGroup())
        self.officer = Group.objects.get(name=self.club.getClubOfficerGroup())
        self.owner = Group.objects.get(name = self.club.getClubOwnerGroup())
        self.club.add_user_to_club(self.officer_user, "Officer")
        self.club.add_user_to_club(self.member_user, "Member")
        self.club.add_user_to_club(self.applicant_user,"Applicant")
        self.club.add_user_to_club(self.user,"Owner")

    def test_owner_url(self):
        self.assertEqual(self.url,'/owner/')

    def test_promote_member_to_officer(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self.member_user.groups.filter(name = self.club.getClubMemberGroup()).exists())
        member_before_count = User.objects.filter(groups__name=self.club.getClubMemberGroup()).count()
        officer_before_count = User.objects.filter(groups__name=self.club.getClubOfficerGroup()).count()
        self.club.switch_user_role_in_club(self.member_user, "Officer")
        member_after_count = User.objects.filter(groups__name=self.club.getClubMemberGroup()).count()
        officer_after_count = User.objects.filter(groups__name=self.club.getClubOfficerGroup()).count()
        self.assertEqual(member_after_count, member_before_count-1)
        self.assertEqual(officer_after_count, officer_before_count+1)

    def test_officer_can_be_demoted(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self.member_user.groups.filter(name = self.club.getClubMemberGroup()).exists())
        officer_before_count = User.objects.filter(groups__name=self.club.getClubMemberGroup()).count()
        member_before_count = User.objects.filter(groups__name=self.club.getClubOfficerGroup()).count()
        self.club.switch_user_role_in_club(self.officer_user, "Member")
        officer_after_count = User.objects.filter(groups__name=self.club.getClubMemberGroup()).count()
        member_after_count = User.objects.filter(groups__name=self.club.getClubOfficerGroup()).count()
        self.assertEqual(officer_after_count, officer_before_count+1)
        self.assertEqual(member_after_count, member_before_count-1)

    def test_officer_can_be_promoted(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self.officer_user.groups.filter(name = self.club.getClubOfficerGroup()).exists())
        self.owner.user_set.add(self.officer_user)
        self.assertTrue(self.user.groups.filter(name=self.club.getClubOwnerGroup()).exists())

    # def test_officer_can_be_demoted(self):
    #     self.client.login(email=self.officer_user.email, password='Password123')
    #     self.assertTrue(self.officer_user.groups.filter(name=self.club.getClubOfficerGroup()).exists())
    #     self.club.switch_user_role_in_club(self.officer_user, "Member")
    #     self.assertTrue(self.officer_user.groups.filter(name = self.club.getClubMemberGroup()).exists())
    #
    # def test_transfer_ownership_to_officer(self):
    #     # response = self.client.post(self.url,self.other_user.id,follow=True)
    #     # response_url = reverse('log_in')
    #     # self.assertRedirects(response,response_url,status_code= 302, target_status_code= 200)
    #     # self.assertTemplateUsed('log_in.html')
    #     # owners = self.owner.user_set.getAll.toList
    #     # current_owner = owners[0]
    #     before_count = User.objects.filter(groups__name=self.club.getClubOwnerGroup()).count()
    #     self.assertTrue(self.user.groups.filter(name=self.club.getClubOwnerGroup()).exists())
    #     self.assertTrue(self.officer_user.groups.filter(name=self.club.getClubOfficerGroup()).exists())
    #     self.club.switch_user_role_in_club(self.user, "Officer")
    #     self.club.switch_user_role_in_club(self.officer_user, "Owner")
    #     after_count = User.objects.filter(groups__name=self.club.getClubOwnerGroup()).count()
    #     self.assertEqual(before_count, after_count)
    #     self.assertFalse(self.user.groups.filter(name=self.club.getClubOwnerGroup()).exists())
    #     self.assertFalse(self.officer_user.groups.filter(name=self.club.getClubOfficerGroup()).exists())
    #     self.assertTrue(self.officer_user.groups.filter(name=self.club.getClubOwnerGroup()).exists())
    #     self.assertTrue(self.user.groups.filter(name=self.club.getClubOfficerGroup()).exists())
    #

    def test_owner_can_accept_applicants(self):
        self.assertTrue(self.applicant_user.groups.filter(name=self.club.getClubApplicantGroup()).exists())
        self.assertFalse(self.applicant_user.groups.filter(name=self.club.getClubMemberGroup()).exists())
        self.club.switch_user_role_in_club(self.applicant_user, "Member")
        self.assertFalse(self.applicant_user.groups.filter(name=self.club.getClubApplicantGroup()).exists())
        self.assertTrue(self.applicant_user.groups.filter(name=self.club.getClubMemberGroup()).exists())




    # def test_owner_can_view_profile_of_members(self):
    #     driver = webdriver.Chrome()
    #     driver.get('http://localhost:8000/log_in/')
    #     time.sleep(0.001)
    #     username = driver.find_element_by_name('email')
    #     password = driver.find_element_by_name('password')
    #     username.send_keys('billie@example.org')
    #     password.send_keys('Password123')
    #     driver.find_element_by_name('login').click()
    #     driver.find_element_by_name('enter_club').click()
    #     driver.find_element_by_name('members').click()
    #     driver.find_element_by_name('go_to_profile').click()
    #     response = self.selenium.current_url
    #     self.assertEqual(response, 'http://localhost:8000/profile/' + )

    # def test_owner_can_view_profile_of_officers(self):
    #     pass
