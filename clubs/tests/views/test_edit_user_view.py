"""Tests for the profile view."""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from clubs.forms import UserForm
from clubs.models import User
from clubs.tests.helpers import reverse_with_next
from clubs.tests.helpers import LogInTester

class ProfileViewTest(TestCase, LogInTester):
    """Test suite for the profile view."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.other_user = User.objects.get(username='janedoe@example.org')
        self.url = reverse('profile')
        self.form_input = {
            'first_name': 'John2',
            'last_name': 'Doe2',
            'email': 'johndoe2@example.org',
            'bio': 'My bio',
            'personal_statement':'I enjoy chess',
            'experience_level': 'Beginner'
        }

    def test_profile_url(self):
        self.assertEqual(self.url, '/profile/')

    def test_get_profile(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserForm))
        self.assertEqual(form.instance, self.user)


    def test_unsuccesful_profile_update(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form_input['email'] = 'janedoe@example.org'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input,follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserForm))
        self.assertFalse(form.is_bound)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'johndoe@example.org')
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.bio, "John Doe from example.org")
        self.assertEqual(self.user.experience_level, "Beginner")
        self.assertEqual(self.user.personal_statement, "I love chess")

    def test_unsuccessful_profile_update_due_to_duplicate_username(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in)
        self.form_input['email'] = 'janedoe@example.org'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input,follow=True)
        response_url = reverse('profile')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserForm))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'johndoe@example.org')
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.username, 'johndoe@example.org')
        self.assertEqual(self.user.bio, "John Doe from example.org")
        self.assertEqual(self.user.experience_level, "Beginner")
        self.assertEqual(self.user.personal_statement, "I love chess")

    def test_succesful_profile_update(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('profile')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'profile.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John2')
        self.assertEqual(self.user.last_name, 'Doe2')
        self.assertEqual(self.user.email, 'johndoe2@example.org')
        self.assertEqual(self.user.username, 'johndoe2@example.org')
        self.assertEqual(self.user.bio, "My bio")
        self.assertEqual(self.user.experience_level, "Beginner")
        self.assertEqual(self.user.personal_statement, "I enjoy chess")

    def test_post_profile_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url, self.form_input,follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
