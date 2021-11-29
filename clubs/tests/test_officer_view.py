"""Test of the officer view"""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from clubs.forms import LogInForm
from clubs.models import User
from .helpers import LogInTester

class OfficerViewTestCase(TestCase):
    """Tests of the officer view"""
    def setUp(self):
        self.url = reverse('officer')
        self.user = User.objects.create(
            username = 'johndoe@example.org',
            first_name = 'John',
            last_name = 'Doe',
            email = 'johndoe@example.org',
            bio = 'Hello, my name is John Doe',
            personal_statement = 'Hello, my name is John Doe and this is my personal statement',
            password = 'Password123',
        )

    def test_officer_url(self):
        self.assertEqual(self.url, '/officer/')

      
