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

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_user.json',
        'clubs/tests/fixtures/member.json',
        'clubs/tests/fixtures/applicant.json',
    ]

    def setUp(self):
        super().setUpClass()
        self.selenium = WebDriver()

        #self.factory = RequestFactory()

        list_of_clubs = ClubList()
        #list_of_clubs.create_new_club("Cambridge Chessinators", "Cambridge > Oxford", "Cambridge")
        self.club_selenium = list_of_clubs.find_club('Kerbal Chess Club')

        # self.user = User.objects.get(username = "johndoe@example.org")
        self.url = reverse('officer')
        self.url_selenium = 'http://localhost:8000/officer/'

    def tearDown(self):
        self.selenium.quit()
        super().tearDown()

    def test_officer_url(self):
        self.assertEqual(self.url,'/officer/')

    def test_get_owner_view(self):
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
        #request = self.factory.get('/group_check/')
        #request.user = self.user
        self.assertEqual(response, self.url_selenium)
