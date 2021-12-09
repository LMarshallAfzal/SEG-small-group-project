"""Unit tests of the create club form."""
from django import forms
from django.test import TestCase
from clubs.forms import CreateClubForm
from clubs.models import Club
from clubs.club_list import ClubList

class CreateClubFormTestCase(TestCase):
    """Unit tests of the create club form."""
    def setUp(self):
        self.form_input = {
            'club_name': 'Test chess team',
            'mission_statement': 'The mission statement of the test team',
            }

    def test_form_accepts_valid_input(self):
        form = CreateClubForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_contains_required_fields(self):
        form = CreateClubForm()
        self.assertIn('club_name', form.fields)
        self.assertIn('mission_statement', form.fields)
        self.assertIn('location', form.fields)

    def test_form_rejects_blank_club_name(self):
        self.form_input['club_name'] = ''
        form = CreateClubForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_blank_mission_statement(self):
        self.form_input['mission_statement'] = ''
        form = CreateClubForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_blank_mission_statement(self):
        self.form_input['mission_statement'] = ''
        form = CreateClubForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_blank_location(self):
        self.form_input['location'] = ''
        form = CreateClubForm(data=self.form_input)
        self.assertTrue(form.is_valid())
