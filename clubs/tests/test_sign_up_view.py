from django.test import TestCase
from clubs.forms import SignUpForm
from clubs.models import User
from django.urls import reverse
from .helpers import LogInTester
from django.contrib.auth.hashers import check_password

class SignUpViewTestCase(TestCase, LogInTester):

    fixtures = ['clubs/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('sign_up')
        self.form_input = {
            'first_name': 'Jack',
            'last_name': 'Henwood',
            'email': 'jackhenwood@example.org',
            'bio': 'My bio',
            'new_password': 'Password123',
            'password_confirmation': 'Password123',
            'personal_statment': 'chess vibes',
            'experience_level': 'Beginner'
        }
        self.user = User.objects.get(username='johndoe@example.org')

    def test_sign_up_url(self):
        self.assertEqual(self.url, '/sign_up/')

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
        redirect_url = reverse('profile')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_unsuccessful_sign_up(self):
        self.form_input['email'] = 'BAD_EMAIL@@EXAMPLE.ORG'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_successful_sign_up(self):
        before_count = User.objects.count()
        #The line below also fails and I dont know
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count + 1)
        #The line below fails because of this error AssertionError: '/show_current_user_profile/' != '/profile'
        response_url = reverse('profile')
        self.assertRedirects(response, response_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'profile.html')
        user = User.objects.get(first_name = 'Jack')
        self.assertEqual(user.first_name, 'Jack')
        self.assertEqual(user.last_name, 'Henwood')
        self.assertEqual(user.email, 'jackhenwood@example.org')
        self.assertEqual(user.bio, 'My bio')
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)
        self.assertTrue(self._is_logged_in())

    def test_post_sign_up_redirects_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow = True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        #The line below fails because of this error AssertionError: '/show_current_user_profile/' != '/profile'
        redirect_url = reverse('profile')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'profile.html')
