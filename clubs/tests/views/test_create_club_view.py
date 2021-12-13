"""Unit tests of the create club form."""
from django.test import TestCase
from clubs.forms import CreateClubForm
from clubs.models import Club
from django.urls import reverse
from clubs.club_list import ClubList


class CreateClubViewTestCase(TestCase):
    """Unit tests of the create club form."""
    def setUp(self):
        self.url = reverse('create_new_club')
        self.form_input = {
            'club_name': 'Test chess team',
            'mission_statement': 'The mission statement of the test team',
            'location': 'Aldwych'
        }

    def test_create_club_url(self):
        self.assertEqual(self.url,'/create_new_club/')

    def test_get_create_new_club(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_club_form.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CreateClubForm))
        self.assertFalse(form.is_bound)
