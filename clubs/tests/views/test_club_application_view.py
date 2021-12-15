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
        'clubs/tests/fixtures/club.json',
    ]

    def setUp(self):
        self.url = reverse('application_form')
        self.form_input = {
            "first_name": 'Jack',
            "last_name": 'Henwood',
            "email": 'jackhenwood@example.org',
            "bio": 'My bio',
            "experience_level": 'Beginner',
            "personal_statement": 'My personal statement!'
        }


    """The fields should be filled in automatically when a user enters this form,
       as they would be logged in already. How to test this likely involves creating
       and logging in a user first, how to do this?"""
