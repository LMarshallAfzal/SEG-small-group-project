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

    def setUp(self):
        super().setUpClass()
        self.selenium = WebDriver()

        list_of_clubs = ClubList()
        self.club_selenium = list_of_clubs.find_club('Kerbal Chess Club')

        self.url = reverse('member_list')
        self.url_selenium = 'http://localhost:8000/member_list/'

    def tearDown(self):
        self.selenium.quit()
        super().tearDown()

    def test_member_url(self):
        self.assertEqual(self.url,'/member_list/')

    def test_get_member_view(self):
        self.selenium.get('http://localhost:8000/log_in/')
        time.sleep(0.00001)
        username = self.selenium.find_element_by_name('email')
        password = self.selenium.find_element_by_name('password')
        username.send_keys('jeb@example.org')
        password.send_keys('Password123')
        self.selenium.find_element_by_name('login').click()
        self.selenium.find_element_by_name('enter_club').click()
        time.sleep(0.00001)
        response = self.selenium.current_url
        self.assertEqual(response, self.url_selenium)

    # def test_redirect_when_not_owner(self):
    #     self.selenium.get('http://localhost:8000/log_in/')
    #     time.sleep(0.00001)
    #     username = self.selenium.find_element_by_name('email')
    #     password = self.selenium.find_element_by_name('password')
    #     username.send_keys('val@example.org')
    #     password.send_keys('Password123')
    #     self.selenium.find_element_by_name('login').click()
    #     self.selenium.find_element_by_name('enter_club').click()
    #     self.selenium.get('http://localhost:8000/member_list/')
    #     time.sleep(0.00001)
    #     response = self.selenium.current_url
    #     self.assertEqual(response,'http://localhost:8000/profile/')
