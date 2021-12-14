"""Unit tests of the User model"""
from django.test import TestCase
from clubs.models import User
from django.core.exceptions import ValidationError

class UserModelTestCase(TestCase):
    """Unit tests of the User model"""
    def setUp(self):
        self.user = User.objects.create_user(
        '@jarredbowen',
        first_name = 'Jarred',
        last_name = 'Bowen',
        email = 'jarredbowen@example.org',
        bio = 'Hi, I am jarred',
        experience_level = 'Beginner',
        personal_statement = 'I like to play chess!',
        )

    """Tests for the first_name field"""
    def test_first_name_must_not_be_blank(self):
        self.user.first_name = ''
        self._assert_user_is_invalid()

    def test_first_name_can_be_repeated(self):
        second_user = self._create_second_user()
        self.user.first_name = second_user.first_name
        self._assert_user_is_valid()

    def test_first_name_can_be_50_characters_long(self):
        self.user.first_name = 'x' *50
        self._assert_user_is_valid()

    def test_first_name_can_not_be_longer_50_characters_long(self):
        self.user.first_name = 'x' *51
        self._assert_user_is_invalid()


    """Tests for the last_name field"""
    def test_last_name_must_not_be_blank(self):
        self.user.last_name = ''
        self._assert_user_is_invalid()

    def test_last_name_can_be_repeated(self):
        second_user = self._create_second_user()
        self.user.last_name = second_user.last_name
        self._assert_user_is_valid()

    def test_last_name_can_be_50_characters_long(self):
        self.user.last_name = 'x' *50
        self._assert_user_is_valid()

    def test_last_name_can_not_be_longer_50_characters_long(self):
        self.user.last_name = 'x' *51
        self._assert_user_is_invalid()


    """Tests for the email field"""
    def test_email_must_not_be_blank(self):
        self.user.email = ''
        self._assert_user_is_invalid()

    def test_email_must_contain_domain_name(self):
        self.user.email = 'johndoe@example'
        self._assert_user_is_invalid()

    def test_email_must_not_contain_more_than_one_at(self):
        self.user.email = 'johndoe@@example.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_at_symbol(self):
        self.user.email = 'johndoe.example.org'
        self._assert_user_is_invalid()

    def test_email_must_be_unique(self):
        User.objects.create_user(
        '@Bendoe',
        first_name = 'Ben',
        last_name = 'Doe',
        email = 'bendoe@example.org',
        bio = 'I am ben',
        experience_level = 'Advanced',
        personal_statement = 'I am a winner!'

        )
        self.user.email = 'bendoe@example.org'
        self._assert_user_is_invalid()

    def test_email_is_not_case_sensitive(self):
        second_user = self._create_second_user()
        second_user.email = 'JARREDBOWEN@example.org'
        self.client.login(email = second_user.email, password = 'Password123') #Change to assert form is valid?

    """Tests for the bio field"""
    def test_bio_may_be_blank(self):
        self.user.bio = ''
        self._assert_user_is_valid()

    def test_bio_may_be_520_characters_long(self):
        self.user.bio = 'x' * 520
        self._assert_user_is_valid()

    def test_bio_may_not_be_520_characters_long(self):
        self.user.bio = 'x' * 521
        self._assert_user_is_invalid()

    def test_bio_does_not_need_to_be_unique(self):
        second_user = self._create_second_user()
        self.user.bio = second_user.bio
        self._assert_user_is_valid()


        """Tests for the experience_level field"""
    def test_experience_level_must_be_one_of_the_choices(self):
        self.user.experience_level = 'Beginner' or 'Intermediate' or 'Advanced'
        self._assert_user_is_valid()

    def test_experience_level_must_not_be_outside_of_the_choices(self):
        self.user.experience_level = 'Medium'
        self._assert_user_is_invalid()

    def test_experience_level_may_be_12_characters_long(self):
        self.user.experience_level = 'Intermediate'
        self._assert_user_is_valid()

    def test_experience_level_may_not_be_13_characters_long(self):
        self.user.experience_level = 'x' * 13
        self._assert_user_is_invalid()


    """Tests for the personal_statement field"""
    def test_personal_statement_can_be_blank(self):
        self.user.personal_statement = ''
        self._assert_user_is_valid()

    def test_personal_statement_may_be_1250_characters_long(self):
        self.user.personal_statement = 'x' * 1250
        self._assert_user_is_valid()

    def test_personal_statement_may_not_be_1251_characters_long(self):
        self.user.personal_statement = 'x' * 1251
        self._assert_user_is_invalid()

# Should I uncomment this method?
    # def test_personal_statement_does_not_need_to_be_unique(self):
    #     second_user = self._create_second_user()
    #     self.user.personal_statement = second_user.personal_statement
    #     self._assert_user_is_valid()



    def _create_second_user(self):
        user = User.objects.create_user(
        '@jaredbowen',
        first_name = 'Jarred',
        last_name = 'Bowen',
        email = 'jaredbowen@example.org',
        bio = 'Hi, I am jarred',
        experience_level = 'Beginner',
        personal_statement = 'I like to play chess!',
        )
        return user

    def test_valid_user(self):
        self._assert_user_is_valid()


    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except(ValidationError):
            self.fail('Test user should be valid')


    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()
