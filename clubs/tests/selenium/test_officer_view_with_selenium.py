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

class OfficerSeleniumTestCase(unittest.TestCase):
    """Unit tests of the user form."""

    def setUp(self):
        super().setUpClass()
        self.selenium = WebDriver()

        list_of_clubs = ClubList()
        self.club_selenium = list_of_clubs.find_club('Kerbal Chess Club')

        self.url = reverse('officer')
        self.url_selenium = 'http://localhost:8000/officer/'

    def tearDown(self):
        self.selenium.quit()
        super().tearDown()

    def test_officer_url(self):
        self.assertEqual(self.url,'/officer/')

    def test_get_officer_view(self):
        self.selenium.get('http://localhost:8000/log_in/')
        time.sleep(0.00001)
        username = self.selenium.find_element_by_name('email')
        password = self.selenium.find_element_by_name('password')
        username.send_keys('val@example.org')
        password.send_keys('Password123')
        self.selenium.find_element_by_name('login').click()
        self.selenium.find_element_by_name('enter_club').click()
        time.sleep(0.00001)
        response = self.selenium.current_url
        self.assertEqual(response, self.url_selenium)

    def test_redirect_when_not_officer(self):
        self.selenium.get('http://localhost:8000/log_in/')
        time.sleep(0.00001)
        username = self.selenium.find_element_by_name('email')
        password = self.selenium.find_element_by_name('password')
        username.send_keys('jeb@example.org')
        password.send_keys('Password123')
        self.selenium.find_element_by_name('login').click()
        self.selenium.find_element_by_name('enter_club').click()
        self.selenium.get('http://localhost:8000/officer/')
        time.sleep(0.00001)
        response = self.selenium.current_url
        self.assertEqual(response,'http://localhost:8000/profile/')

    def test_officer_can_accept_applicants(self):
        self.selenium.get('http://localhost:8000/log_in/')
        time.sleep(0.0001)
        username = self.selenium.find_element_by_name('email')
        password = self.selenium.find_element_by_name('password')
        username.send_keys('val@example.org')
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

    def test_officer_can_reject_applicants(self):
        self.selenium.get('http://localhost:8000/log_in/')
        time.sleep(0.001)
        username = self.selenium.find_element_by_name('email')
        password = self.selenium.find_element_by_name('password')
        username.send_keys('val@example.org')
        password.send_keys('Password123')
        self.selenium.find_element_by_name('login').click()
        self.selenium.find_element_by_name('enter_club').click()
        self.selenium.find_element_by_name('applicants').click()
        before_count = User.objects.filter(groups__name = self.club_selenium.getClubApplicantGroup()).count()
        self.selenium.find_element_by_name('reject').click()
        time.sleep(0.001)
        after_count = User.objects.filter(groups__name = self.club_selenium.getClubApplicantGroup()).count()
        self.assertEqual(before_count-1, after_count)
