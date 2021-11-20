"""User model test cases"""
from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import User

"""User model test cases"""
class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            '@johndoe',
            first_name = 'John',
            last_name = 'Doe',
            email = 'johndoe@example.org',
            bio = 'The quick brown fox jumps over the lazy dog',
            experience_level = User.BEGINNER,
            personal_statement = 'Relatively new player interested in chess'
        )

    #Note that we start the method with _ to show it is not a test method?
    def _create_second_user(self):
        return User.objects.create_user(
            '@janedoe',
            first_name = 'Jane',
            last_name = 'Doe',
            email = 'janedoe@example.org',
            bio = 'This is Jane\'s profile',
            experience_level = User.INTERMEDIATE,
            personal_statement = 'Regular casual chess player looking for a challenge'
        )

    #Tests a user which we know should be valid, to make sure something isn't wrong with the creation in setUp()
    def test_valid_user(self):
        self.assert_user_is_valid()


    """username field tests - by default usernames must not be blank and be unique"""
    def test_username_cannot_be_blank(self):
        self.user.username = ''
        self.assert_user_is_invalid()

    def test_username_must_be_unique(self):
        second_user = self._create_second_user()
        self.user.username = second_user.username
        self.assert_user_is_invalid()


    """first_name field tests"""
    def test_firstName_cannot_be_blank(self):
        self.user.first_name = ""
        self.assert_user_is_invalid()

    def test_firstName_may_already_exist(self):
        second_user = self._create_second_user()
        self.user.first_name = second_user.first_name
        self.assert_user_is_valid()

    def test_firstName_can_be_50_characters_long(self):
        self.user.first_name = "x" * 50
        self.assert_user_is_valid()

    def test_firstName_cannot_be_51_characters_long(self):
        self.user.first_name = "x" * 51
        self.assert_user_is_invalid()


    """last_name field tests"""
    def test_lastName_cannot_be_blank(self):
        self.user.last_name = ""
        self.assert_user_is_invalid()

    def test_lastName_may_already_exist(self):
        second_user = self._create_second_user()
        self.user.last_name = second_user.last_name
        self.assert_user_is_valid()

    def test_lastName_can_be_50_characters_long(self):
        self.user.last_name = "x" * 50
        self.assert_user_is_valid()

    def test_lastName_cannot_be_51_characters_long(self):
        self.user.last_name = "x" * 51
        self.assert_user_is_invalid()


    """Email field tests"""
    def test_email_must_not_be_blank(self):
        self.user.email = ''
        self.assert_user_is_invalid()

    def test_email_must_be_unique(self):
        second_user = self._create_second_user()
        self.user.email = second_user.email
        self.assert_user_is_invalid()

    def test_email_starts_with_username(self):
        self.user.email = '@example.org'
        self.assert_user_is_invalid()

    def test_email_must_contain_at_symbol(self):
        self.user.email = 'johndoeexmaple.org'
        self.assert_user_is_invalid()

    def test_email_must_contain_only_one_at(self):
        self.user.email = 'johndoe@@example.org'
        self.assert_user_is_invalid()

    def test_email_must_contain_domain_name(self):
        self.user.email = 'johndoe@.org'
        self.assert_user_is_invalid()

    def test_email_must_contain_domain(self):
        self.user.email = 'johndoe@example'
        self.assert_user_is_invalid()


    """Bio field tests"""
    def test_bio_cannot_be_blank(self):
        self.user.bio = ''
        self.assert_user_is_invalid()

    def test_bio_does_not_have_to_be_unique(self):
        second_user = self._create_second_user()
        self.user.bio = second_user.bio
        self.assert_user_is_valid()

    def test_bio_can_be_520_characters(self):
        self.user.bio = 'x' * 520
        self.assert_user_is_valid()

    def test_bio_cannot_be_521_characters(self):
        self.user.bio = 'x' * 521
        self.assert_user_is_invalid()


    """experience_level field tests"""
    #No tests currently

    """personal_statement field tests"""
    def test_personal_statement_cannot_be_blank(self):
        self.user.personal_statement = ''
        self.assert_user_is_invalid()

    def test_personal_statement_does_not_have_to_be_unique(self):
        second_user = self._create_second_user()
        self.user.personal_statement = second_user.personal_statement
        self.assert_user_is_valid()

    def test_personal_statement_can_be_1250_characters(self):
        self.user.personal_statement = 'x' * 1250
        self.assert_user_is_valid()

    def test_personal_statement_cannot_be_1251_characters(self):
        self.user.personal_statement = 'x' * 1251
        self.assert_user_is_invalid()

    """Asserts for all user field tests through use of full_clean()"""
    def assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()
