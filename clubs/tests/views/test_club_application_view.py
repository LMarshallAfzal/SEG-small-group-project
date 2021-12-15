"""Tests for the club application view"""
from django.test import TestCase
from django.urls import reverse
from clubs.forms import ApplicationForm
from clubs.models import User, Club

def ClubApplicationViewTestCase(TestCase):
    """Tests for the club application view"""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_user.json',
<<<<<<< HEAD
        'clubs/tests/fixtures/club.json'
=======
        'clubs/tests/fixtures/club.json',
>>>>>>> bdc6b405745b4e4e598e189e5518001f3437ff54
    ]

    def setUp(self):
        self.url = reverse('application_form')
<<<<<<< HEAD
        #Form input based on user fixture
        self.form_input = {
            "first_name": 'John',
            "last_name": 'Doe',
            "email": 'johndoe@example.org',
            "bio": 'John Doe from example.org',
            "experience_level": 'Beginner',
            "personal_statement": 'I love chess'
=======
        self.form_input = {
            "first_name": 'Jack',
            "last_name": 'Henwood',
            "email": 'jackhenwood@example.org',
            "bio": 'My bio',
            "experience_level": 'Beginner',
            "personal_statement": 'My personal statement!'
>>>>>>> bdc6b405745b4e4e598e189e5518001f3437ff54
        }


    """The fields should be filled in automatically when a user enters this form,
<<<<<<< HEAD
       as they would be logged in already, how to do this?"""
=======
       as they would be logged in already. How to test this likely involves creating
       and logging in a user first, how to do this?"""
>>>>>>> bdc6b405745b4e4e598e189e5518001f3437ff54
