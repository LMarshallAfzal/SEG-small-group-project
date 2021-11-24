from clubs.forms import SignUpForm
from clubs.models import User
from django.test import TestCase
from django import forms
from django.contrib.auth.hashers import check_password


class SignUpFormTestCase(TestCase):
    def setUp(self):
        self.form_input = {
        "first_name": 'Jack',
        "last_name": 'Henwood',
        "email": 'jackhenwood@example.org',
        "bio": 'My bio',
        "experience_level": 'BEGINNER',
        "personal_statement": 'My personal statement!',
        "new_password": 'Password123',
        "password_confirmation": 'Password123'
        }

    def test_sign_up_form_accepts_valid_input(self):
        form = SignUpForm(data = self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = SignUpForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))
        self.assertIn('bio', form.fields)
        self.assertIn('new_password', form.fields)
        new_password_widget = form.fields['new_password'].widget
        self.assertTrue(isinstance(new_password_widget, forms.PasswordInput))
        self.assertIn('password_confirmation', form.fields)
        password_confirmation_widget = form.fields['password_confirmation'].widget
        self.assertTrue(isinstance(password_confirmation_widget, forms.PasswordInput))

    # def test_form_uses_model_validation(self):
    #     self.form_input['username'] = 'badusername'
    #     form = SignUpForm(data = self.form_input)
    #     self.assertFalse(form.is_valid())

    def test_password_must_contain_uppercase_character(self):
        self.form_input['new_password'] = 'password123'
        self.form_input['password_confirmation'] = 'password123'
        form = SignUpForm(data = self.form_input)
        self.assertFalse(form.is_valid())


    def test_password_must_contain_lowercase_character(self):
        self.form_input['new_password'] = 'PASSWORD123'
        self.form_input['password_confirmation'] = 'PASSWORD123'
        form = SignUpForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.form_input['new_password'] = 'Password'
        self.form_input['password_confirmation'] = 'Password'
        form = SignUpForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_and_password_confirmation_are_identical(self):
        self.form_input['password_confirmation'] = 'WrongPassword123'
        form = SignUpForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_saves_correctly(self):
        form = SignUpForm(data = self.form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        # self.assertEqual(after_count, before_count + 1)
        user = User.objects.get(first_name = 'Jack')
        self.assertEqual(user.first_name, 'Jack')
        self.assertEqual(user.last_name, 'Henwood')
        self.assertEqual(user.email, 'jackhenwood@example.org')
        self.assertEqual(user.bio, 'My bio')
        self.assertEqual(user.experience_level, 'BEGINNER')
        self.assertEqual(user.personal_statement, 'My personal statemnet!')
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)
