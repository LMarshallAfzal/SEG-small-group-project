from django.test import LiveServerTestCase
from selenium import webdriver
import time
from clubs.club_list import ClubList
from clubs.models import User, Group, Club


class InitialTest(LiveServerTestCase):

    fixtures = [
        'clubs/tests/fixtures/default_user.json']


    def testhomepage(driver):
        list_of_clubs = ClubList()
        list_of_clubs.create_new_club("Cambridge Chessinators", "Cambridge > Oxford", "Cambridge")
        for club in list_of_clubs.club_list:
                print(club.club_name)
        club = list_of_clubs.find_club("Cambridge Chessinators")
        user = User.objects.get(email = "johndoe@example.org")
        owner = Group.objects.get(name = club.getClubOwnerGroup())
        club.add_user_to_club(user, "Owner")



        driver = webdriver.Firefox()
        driver.get('http://localhost:8000/')
        time.sleep(3)
        driver.find_element_by_name("login").click()
        time.sleep(3)
        username = driver.find_element_by_name("email")
        password = driver.find_element_by_name("password")
        username.send_keys('johndoe@example.org')
        password.send_keys('Password123')
        driver.find_element_by_name("login").click()
        time.sleep(3)
        driver.find_element_by_name("enter_club").click()
        driver.get('http://localhost:8000/owner')
        time.sleep(3000000)


    def testvalpage(driver):
        driver = webdriver.Chrome()
        driver.get('http://localhost:8000/')
        time.sleep(1)
        driver.find_element_by_name("login").click()
        time.sleep(1)
        username = driver.find_element_by_name("email")
        password = driver.find_element_by_name("password")
        username.send_keys('val@example.org')
        password.send_keys('Password123')
        driver.find_element_by_name("login").click()
        time.sleep(1)
        