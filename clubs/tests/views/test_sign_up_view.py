"""Tests of the sign up view."""
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from clubs.forms import SignUpForm
from clubs.models import User
from clubs.tests.helpers import LogInTester

class SignUpViewTestCase(TestCase, LogInTester):
    """Tests of the sign up view."""

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_user.json',
    ]

    def setUp(self):
        self.url = reverse('sign_up')
        self.form_input = {
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'johnsmith@example.org',
            'bio': 'My bio',
            'new_password': 'Password123',
            'password_confirmation': 'Password123',
            'personal_statement':'Hi',
            'experience_level':'Beginner'
        }
        self.user = User.objects.get(username='johndoe@example.org')

    def test_sign_up_url(self):
        self.assertEqual(self.url,'/sign_up/')

    def test_get_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertFalse(form.is_bound)

    def test_get_sign_up_redirects_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('club_selection')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'club_selection.html')
    
    def test_unsuccesful_sign_up(self):
        self.form_input['email'] = 'jodo@@kungfu.org'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        form = response.context['form']
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.is_bound)
        self.assertTemplateUsed(response, 'sign_up.html')
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())
    
    def test_succesful_sign_up(self):
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)
        response_url = reverse('club_selection')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'club_selection.html')
        user = User.objects.get(username='janedoe@example.org')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'janedoe@example.org')
        self.assertEqual(user.bio, 'Jane Doe from example.org')
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)
        self.assertTrue(self._is_logged_in())
    
    def test_post_sign_up_redirects_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        redirect_url = reverse('club_selection')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'club_selection.html')
