"""Tests for the club application form"""
from clubs.forms import ApplicationForm
from clubs.models import Club
from django.test import TestCase
from django import forms
from clubs.club_list import ClubList

class ClubApplicationFormTestCase(TestCase):
    """Tests for the club application form"""
    def setUp(self):
        self.list_of_clubs = ClubList()
        self.list_of_clubs.create_new_club(
            name = "The Buzzards",
            mission_statement = "Scavenging wastelander tribe of bandits",
            location = "The sunken city"
        )
        self.club = list_of_clubs.find_club("The Buzzards")
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
        self.assertIn('experience_level', form.fields)
        self.assertIn('personal_statement', form.fields)

    def test_form_uses_model_validation(self):
        self.form_input['email'] = 'BAD_EMAIL@@email.org'
        form = ApplicationForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    # def test_form_saves_correctly(self):
    #     form = ApplicationForm(data = self.form_input)
    #     before_role = Club.
    #     form.save()
    #     after_count = User.objects.count()
    #     self.assertEqual(after_count, before_count + 1)
    #     user = User.objects.get(first_name = 'Jack')
    #     self.assertEqual(user.first_name, 'Jack')
    #     self.assertEqual(user.last_name, 'Henwood')
    #     self.assertEqual(user.username, 'jackhenwood@example.org')
    #     self.assertEqual(user.bio, 'My bio')
    #     self.assertEqual(user.experience_level, 'Beginner')
    #     self.assertEqual(user.personal_statement, 'My personal statement!')
    #     is_password_correct = check_password('Password123', user.password)
    #     self.assertTrue(is_password_correct)
