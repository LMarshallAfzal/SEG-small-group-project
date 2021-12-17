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


class UserFormTestCase(unittest.TestCase):
    """Unit tests of the user form."""


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
