from django.test import LiveServerTestCase
from selenium import webdriver

class InitialTest(LiveServerTestCase):
    def testhomepage(driver):
        driver = webdriver.Chrome()
        driver.get('localhost:8000')
        log_in = driver.find_element_by_class_name('Log in')
        