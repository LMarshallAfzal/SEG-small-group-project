from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase, LiveServerTestCase
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

    def setUp(self):
        super().setUp()
        self.selenium = WebDriver()


        self.list_of_clubs = ClubList()
        self.club_selenium = self.list_of_clubs.find_club('Kerbal Chess Club')

        self.url = reverse('owner')
        self.url_selenium = 'http://localhost:8000/owner/'

    def tearDown(self):
        self.selenium.quit()
        super().tearDown()

    def test_owner_url(self):
        self.assertEqual(self.url,'/owner/')

    def test_get_owner_view(self):
        self.selenium.get('http://localhost:8000/log_in/')
        time.sleep(0.5)
        username = self.selenium.find_element_by_name('email')
        password = self.selenium.find_element_by_name('password')
        username.send_keys('billie@example.org')
        password.send_keys('Password123')
        self.selenium.find_element_by_name('login').click()
        self.selenium.find_element_by_name('enter_club').click()
        time.sleep(0.5)
        response = self.selenium.current_url
        self.assertEqual(response, self.url_selenium)

    def test_redirect_when_not_owner(self):
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

    def test_promote_member_to_officer(self):
        self.selenium.get('http://localhost:8000/log_in/')
        time.sleep(0.001)
        username = self.selenium.find_element_by_name('email')
        password = self.selenium.find_element_by_name('password')
        username.send_keys('billie@example.org')
        password.send_keys('Password123')
        self.selenium.find_element_by_name('login').click()
        self.selenium.find_element_by_name('enter_club').click()
        self.selenium.find_element_by_name('members').click()
        before_count = User.objects.filter(groups__name = self.club_selenium.getClubMemberGroup()).count()
        self.selenium.find_element_by_name('promote').click()
        time.sleep(0.001)
        after_count = User.objects.filter(groups__name = self.club_selenium.getClubMemberGroup()).count()
        self.assertEqual(before_count-1, after_count)

    def test_officer_can_be_demoted(self):
        self.selenium.get('http://localhost:8000/log_in/')
        time.sleep(0.001)
        username = self.selenium.find_element_by_name('email')
        password = self.selenium.find_element_by_name('password')
        username.send_keys('billie@example.org')
        password.send_keys('Password123')
        self.selenium.find_element_by_name('login').click()
        self.selenium.find_element_by_name('enter_club').click()
        self.selenium.find_element_by_name('officers').click()
        before_count = User.objects.filter(groups__name = self.club_selenium.getClubOfficerGroup()).count()
        self.selenium.find_element_by_name('demote').click()
        time.sleep(0.001)
        after_count = User.objects.filter(groups__name = self.club_selenium.getClubOfficerGroup()).count()
        self.assertEqual(before_count-1, after_count)


    def test_owner_can_accept_applicants(self):
        self.selenium.get('http://localhost:8000/log_in/')
        time.sleep(0.001)
        username = self.selenium.find_element_by_name('email')
        password = self.selenium.find_element_by_name('password')
        username.send_keys('billie@example.org')
        password.send_keys('Password123')
        self.selenium.find_element_by_name('login').click()
        self.selenium.find_element_by_name('enter_club').click()
        self.selenium.find_element_by_name('applicants').click()
        applicant_before_count = User.objects.filter(groups__name = self.club_selenium.getClubApplicantGroup()).count()
        member_before_count = User.objects.filter(groups__name = self.club_selenium.getClubMemberGroup()).count()
        self.selenium.find_element_by_name('accept').click()
        time.sleep(0.001)
        applicant_after_count = User.objects.filter(groups__name = self.club_selenium.getClubApplicantGroup()).count()
        member_after_count = User.objects.filter(groups__name = self.club_selenium.getClubMemberGroup()).count()
        self.assertEqual(applicant_before_count-1, applicant_after_count)
        self.assertEqual(member_before_count+1, member_after_count)

    def test_owner_can_reject_applicants(self):
        driver = webdriver.Chrome()
        driver.get('http://localhost:8000/log_in/')
        time.sleep(0.0001)
        username = driver.find_element_by_name('email')
        password = driver.find_element_by_name('password')
        username.send_keys('billie@example.org')
        password.send_keys('Password123')
        driver.find_element_by_name('login').click()
        driver.find_element_by_name('enter_club').click()
        driver.find_element_by_name('applicants').click()
        before_count = User.objects.filter(groups__name = self.club_selenium.getClubApplicantGroup()).count()
        driver.find_element_by_name('reject').click()
        time.sleep(0.0001)
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
