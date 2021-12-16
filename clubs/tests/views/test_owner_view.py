"""Test of the officer view"""
#from django.test import TestCase, LiveServerTestCase, RequestFactory
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
import time
import unittest
from django.urls import reverse
from clubs.models import User, Club
from django.contrib.auth.models import Group
from clubs.club_list import ClubList
from clubs.views import group_check

#TestCase, LiveServerTestCase):

class UserFormTestCase(unittest.TestCase):
    """Unit tests of the user form."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_user.json',
        'clubs/tests/fixtures/member.json',
        'clubs/tests/fixtures/applicant.json',
    ]

#To do fix tests
    def setUp(self):
        super().setUpClass()
        self.selenium = WebDriver()

        #self.factory = RequestFactory()

        list_of_clubs = ClubList()
        #list_of_clubs.create_new_club("Cambridge Chessinators", "Cambridge > Oxford", "Cambridge")
        self.club_selenium = list_of_clubs.find_club('Kerbal Chess Club')

        # self.user = User.objects.get(username = "johndoe@example.org")
        self.url = reverse('owner')
        self.url_selenium = 'http://localhost:8000/owner/'
        # self.officer_user = User.objects.get(username = 'janedoe@example.org')
        #self.member_user = User.objects.get(username = 'petrapickles@example.org')
        #self.applicant_user = User.objects.get(username = 'peterpickles@example.org')

        # self.owner = Group.objects.get(name = self.club.getClubOwnerGroup())
        # self.club.add_user_to_club(self.user, "Owner")
        #
        # self.officer = Group.objects.get(name = self.club.getClubOfficerGroup())
        # self.club.add_user_to_club(self.officer_user, "Officer")

        # self.member = Group.objects.get(name = self.club.getClubMemberGroup())
        # self.club.add_user_to_club(self.member_user, "Member")
        #
        # self.applicant = Group.objects.get(name = self.club.getClubApplicantGroup())
        # self.club.add_user_to_club(self.applicant_user,"Applicant")

    def tearDown(self):
        self.selenium.quit()
        super().tearDown()

    # def _login_with_selenium(self):

    def test_owner_url(self):
        #response = group_check(request)
        self.assertEqual(self.url,'/owner/')

    def test_get_owner_view(self):
        self.selenium.get('http://localhost:8000/log_in/')
        time.sleep(0.00001)
        username = self.selenium.find_element_by_name('email')
        password = self.selenium.find_element_by_name('password')
        username.send_keys('billie@example.org')
        password.send_keys('Password123')
        self.selenium.find_element_by_name('login').click()
        self.selenium.find_element_by_name('enter_club').click()
        time.sleep(0.00001)
        response = self.selenium.current_url
        #request = self.factory.get('/group_check/')
        #request.user = self.user
        self.assertEqual(response, self.url_selenium)

    def test_redirect_when_not_owner(self):
        # driver = webdriver.Chrome()
        self.selenium.get('http://localhost:8000/log_in/')
        time.sleep(0.00001)
        username = self.selenium.find_element_by_name('email')
        password = self.selenium.find_element_by_name('password')
        username.send_keys('val@example.org')
        password.send_keys('Password123')
        self.selenium.find_element_by_name('login').click()
        self.selenium.find_element_by_name('enter_club').click()
        self.selenium.get('http://localhost:8000/owner/')
        time.sleep(0.00001)
        response = self.selenium.current_url
        self.assertEqual(response,'http://localhost:8000/profile/')
        #self.assertTemplateUsed(response, 'profile')


    def test_promote_member_to_officer(self):
        driver = webdriver.Chrome()
        driver.get('http://localhost:8000/log_in/')
        time.sleep(0.001)
        username = driver.find_element_by_name('email')
        password = driver.find_element_by_name('password')
        username.send_keys('billie@example.org')
        password.send_keys('Password123')
        driver.find_element_by_name('login').click()
        driver.find_element_by_name('enter_club').click()
        driver.find_element_by_name('members').click()
        before_count = User.objects.filter(groups__name = self.club_selenium.getClubMemberGroup()).count()
        driver.find_element_by_name('promote').click()
        time.sleep(0.001)
        after_count = User.objects.filter(groups__name = self.club_selenium.getClubMemberGroup()).count()
        self.assertEqual(before_count-1, after_count)
        # self.assertTrue(self.member_user.groups.filter(name = self.club.getClubMemberGroup()).exists())
        # self.assertFalse(self.member_user.groups.filter(name = self.club.getClubOfficerGroup()).exists())
        # self.club.switch_user_role_in_club(self.member_user, "Officer")
        # self.assertTrue(self.member_user.groups.filter(name = self.club.getClubOfficerGroup()).exists())
        # self.assertFalse(self.member_user.groups.filter(name = self.club.getClubMemberGroup()).exists())
        # response = self.client.get(self.url)
        # response_url = reverse('owner_member_list')
        # self.assertRedirects(response,response_url,status_code= 302, target_status_code= 200)
        # self.assertTemplateUsed(response,'owner_member_list')

    def test_officer_can_be_demoted(self):
        driver = webdriver.Chrome()
        driver.get('http://localhost:8000/log_in/')
        time.sleep(0.001)
        username = driver.find_element_by_name('email')
        password = driver.find_element_by_name('password')
        username.send_keys('billie@example.org')
        password.send_keys('Password123')
        driver.find_element_by_name('login').click()
        driver.find_element_by_name('enter_club').click()
        driver.find_element_by_name('officers').click()
        before_count = User.objects.filter(groups__name = self.club_selenium.getClubOfficerGroup()).count()
        driver.find_element_by_name('demote').click()
        time.sleep(0.001)
        after_count = User.objects.filter(groups__name = self.club_selenium.getClubOfficerGroup()).count()
        self.assertEqual(before_count-1, after_count)
        # self.client.login(email=self.user.email, password='Password123')
        # self.assertTrue(self.officer_user.groups.filter(name = self.club.getClubOfficerGroup()).exists())
        # self.club.switch_user_role_in_club(self.officer_user, "Member")
        # self.assertFalse(self.officer_user.groups.filter(name = self.club.getClubOfficerGroup()).exists())
        # self.assertTrue(self.officer_user.groups.filter(name =self.club.getClubMemberGroup()).exists())
        # # response = self.client.get(self.url)
        # response_url = reverse('officer_list')
        # self.assertRedirects(response,response_url,status_code= 302, target_status_code= 200)
        # self.assertTemplateUsed(response,'officer_list.html')


    #def test_cannnot_promote_member_to_owner(self):
        # self.client.login(email=self.user.email, password='Password123')
        # self.assertFalse(self.member_user.groups.filter(name = self.club.getClubOfficerGroup()).exists())
        # self.assertTrue(self.member_user.groups.filter(name = self.club.getClubMemberGroup()).exists())
        # self.club.switch_user_role_in_club(self.member_user, "Owner")
        # self.assertFalse(self.member_user.groups.filter(name= self.club.getClubOwnerGroup).exists())
        # self.assertFalse(self.member_user.groups.filter(name = self.club.getClubOfficerGroup()).exists())
        # response = self.client.get(self.url)
        # response_url = reverse('owner_member_list')
        # self.assertRedirects(response,response_url,status_code= 302, target_status_code= 200)
        # self.assertTemplateUsed(response,'owner_member_list.html')


    # def test_cannnot_promote_applicant_to_owner(self):
    #     self.client.login(email=self.user.email, password='Password123')
    #     self.assertFalse(self.applicant_user.groups.filter(name = self.club.getClubOfficerGroup()).exists())
    #     self.assertFalse(self.applicant_user.groups.filter(name = self.club.getClubMemberGroup()).exists())
    #     self.assertTrue(self.applicant_user.groups.filter(name=self.club.getClubApplicantGroup()).exists())
    #     self.club.switch_user_role_in_club(self.applicant_user, "Owner")
    #     self.assertFalse(self.applicant_user.groups.filter(name= self.club.getClubOwnerGroup).exists())
    #     self.assertFalse(self.applicant_user.groups.filter(name = self.club.getClubOfficerGroup()).exists())
    #     self.assertFalse(self.applicant_user.groups.filter(name = self.club.getClubMemberGroup()).exists())
    #     # response = self.client.get(self.url)
    #     # response_url = reverse('owner_member_list')
    #     # self.assertRedirects(response,response_url,status_code= 302, target_status_code= 200)
    #     # self.assertTemplateUsed(response,'owner_member_list.html')
    #
    #
    # def test_officer_can_be_promoted(self):
    #     self.client.login(email=self.user.email, password='Password123')
    #     self.assertTrue(self.officer_user.groups.filter(name = self.club.getClubOfficerGroup()).exists())
    #     self.owner.user_set.add(self.officer_user)
    #     self.assertTrue(self.user.groups.filter(name=self.club.getClubOwnerGroup()).exists())
    #
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
        driver = webdriver.Chrome()
        driver.get('http://localhost:8000/log_in/')
        time.sleep(0.001)
        username = driver.find_element_by_name('email')
        password = driver.find_element_by_name('password')
        username.send_keys('billie@example.org')
        password.send_keys('Password123')
        driver.find_element_by_name('login').click()
        driver.find_element_by_name('enter_club').click()
        driver.find_element_by_name('applicants').click()
        applicant_before_count = User.objects.filter(groups__name = self.club_selenium.getClubApplicantGroup()).count()
        member_before_count = User.objects.filter(groups__name = self.club_selenium.getClubMemberGroup()).count()
        driver.find_element_by_name('accept').click()
        time.sleep(0.001)
        applicant_after_count = User.objects.filter(groups__name = self.club_selenium.getClubApplicantGroup()).count()
        member_after_count = User.objects.filter(groups__name = self.club_selenium.getClubMemberGroup()).count()
        self.assertEqual(applicant_before_count-1, applicant_after_count)
        self.assertEqual(member_before_count+1, member_after_count)

    def test_owner_can_reject_applicants(self):
        driver = webdriver.Chrome()
        driver.get('http://localhost:8000/log_in/')
        time.sleep(0.001)
        username = driver.find_element_by_name('email')
        password = driver.find_element_by_name('password')
        username.send_keys('billie@example.org')
        password.send_keys('Password123')
        driver.find_element_by_name('login').click()
        driver.find_element_by_name('enter_club').click()
        driver.find_element_by_name('applicants').click()
        before_count = User.objects.filter(groups__name = self.club_selenium.getClubApplicantGroup()).count()
        driver.find_element_by_name('reject').click()
        time.sleep(0.001)
        after_count = User.objects.filter(groups__name = self.club_selenium.getClubApplicantGroup()).count()
        self.assertEqual(before_count-1, after_count)

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
