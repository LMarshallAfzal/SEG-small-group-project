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
        'clubs/tests/fixtures/club.json'
    ]

    def setUp(self):
        self.url = reverse('application_form')
        #Form input based on user fixture
        self.form_input = {
            "first_name": 'John',
            "last_name": 'Doe',
            "email": 'johndoe@example.org',
            "bio": 'John Doe from example.org',
            "experience_level": 'Beginner',
            "personal_statement": 'I love chess'
        }


    """The fields should be filled in automatically when a user enters this form,
       as they would be logged in already, how to do this?"""
