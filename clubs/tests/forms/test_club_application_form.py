"""Tests for the club application form"""
from clubs.forms import ApplicationForm
from clubs.models import User
from django.test import TestCase
from django import forms

class ClubApplicationFormTestCase(TestCase):
    """Tests for the club application form"""
    def setUp(self):
        self.form_input = {
            "first_name": 'Jack',
            "last_name": 'Henwood',
            "email": 'jackhenwood@example.org',
            "bio": 'My bio',
            "experience_level": 'Beginner',
            "personal_statement": 'My personal statement!'
        }

    def test_sign_up_form_accepts_valid_input(self):
        form = ApplicationForm(data = self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = ApplicationForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))
        self.assertIn('bio', form.fields)
