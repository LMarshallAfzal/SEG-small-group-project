"""Unit tests of the log in form."""
from django.contrib import messages
from django import forms
from django.test import TestCase
from clubs.forms import LogInForm
from django.urls import reverse
from django.contrib.auth.models import Group
from clubs.tests.helpers import reverse_with_next
from clubs.models import User

class LogInFormTestCase(TestCase):
    """Unit tests of the log in form."""

    fixtures = ['clubs/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('log_in')
        self.user = User.objects.get(username='johndoe@example.org')

    
    def test_log_in_url(self):
        self.assertEqual(self.url,'/log_in/')

    
    def test_get_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        next = response.context['next']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(next)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    
    def test_get_log_in_with_redirect(self):

        if(self.user.groups.filter(name = 'Member')):
            destination_url = reverse('member_list')
        
        else:
            destination_url = reverse('profile')

        self.url = reverse_with_next('log_in', destination_url)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        next = response.context['next']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertEqual(next, destination_url)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    
    def test_get_log_in_redirects_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        member = Group.objects.get(name = "member")
        check_membership = self.assertIn(self.user,member)
        if(check_membership):
            response = self.client.get(self.url, follow=True)
            redirect_url = reverse('member_list')
            self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
            self.assertTemplateUsed(response, 'member_list.html')
        
        else:
            response = self.client.get(self.url, follow=True)
            redirect_url = reverse('profile')
            self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
            self.assertTemplateUsed(response, 'profile.html')


    def test_form_contains_required_fields(self):
        form = LogInForm()
        self.assertIn('email', form.fields)
        self.assertIn('password', form.fields)
        password_field = form.fields['password']
        self.assertTrue(isinstance(password_field.widget, forms.PasswordInput))

    def test_form_rejects_blank_email(self):
        form_input = { 'username': '', 'password': 'Password123' }
        form = LogInForm(data = form_input)
        form = LogInForm(data = form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_password(self):
        form_input = { 'username': 'johndoe@example.org', 'password': '' }
        form = LogInForm(data = form_input)
        form = LogInForm(data = form_input)
        self.assertFalse(form.is_valid())

    # def test_form_accepts_incorrect_email(self):
    #     self.form_input['email'] = 'example.com'
    #     form = LogInForm(data = self.form_input)
    #     self.assertTrue(form.is_valid())

    def test_form_accepts_incorrect_password(self):
        form_input = { 'username': 'johndoe@example.org', 'password': 'pwd' }
        form = LogInForm(data = form_input)
        self.assertFalse(form.is_valid())

    def test_unsuccesful_log_in(self):
        form_input = { 'username': 'johndoe@example.org', 'password': 'WrongPassword123' }
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)


def test_succesful_log_in_with_redirect(self):
        redirect_url = reverse('member_list')
        form_input = { 'username': 'johndoe@example.org', 'password': 'Password123', 'next': redirect_url }
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'member_list.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
