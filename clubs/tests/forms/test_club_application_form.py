"""Tests for the club application form"""
from clubs.forms import ApplicationForm
from clubs.models import Club
from django.test import TestCase
from django import forms
from clubs.club_list import ClubList

class ClubApplicationFormTestCase(TestCase):
    """Tests for the club application form"""

    fixtures = ['clubs/tests/fixtures/default_user.json']

    def setUp(self):
        #Form input based on user fixture
        self.form_input = {
            "first_name": 'John',
            "last_name": 'Doe',
            "email": 'johndoe@example.org',
            "bio": 'John Doe from example.org',
            "experience_level": 'Beginner',
            "personal_statement": 'I love chess'
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
        self.assertIn('experience_level', form.fields)
        self.assertIn('personal_statement', form.fields)

    def test_form_uses_model_validation(self):
        self.form_input['email'] = 'BAD_EMAIL@@email.org'
        form = ApplicationForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_saves_correctly(self):
        list_of_clubs = ClubList()
        club = self.list_of_clubs.create_new_club(
            name = "The Buzzards",
            mission_statement = "Scavenging wastelander tribe of bandits",
            location = "The sunken city"
            )
        user = User.objects.get(username = "johndoe@example.org")
        form = ApplicationForm(data = self.form_input)
        before_role = self.club.get_user_role_in_club(user)
        self.assertEqual(before_role, None)
        form.save()
        after_role = self.club.get_user_role_in_club(user)
        self.assertEqual(after_role, "Applicant")
