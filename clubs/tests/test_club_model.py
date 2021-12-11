"""Unit tests of the Club model as well as the groups created by the club"""
from django.test import TestCase
from clubs.models import Club, User
from django.core.exceptions import ValidationError
import clubs.helpers

class ClubModelTestCase(TestCase):
    """Unit tests of the Club model as well as the groups created by the club"""
    def setUp(self):
        #We do not use the ClubList class to create the new club model instance so that this remains a model test
        self.club = Club.objects.create_club(
            name = "Generic chess club",
            mission_statement = "Play chess here",
            location = "London"
            )

    def _create_second_club(self):
        second_club = Club.objects._create_club(
            name = "Even more generic chess club",
            mission_statement = "Play chess",
            location = "Somewhere"
        )

    def _create_new_user(self):
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

    def test_valid_club(self):
        self._assert_club_is_valid()

    """Tests for club_name field"""
    def test_club_name_must_not_be_blank(self):
        self.club.club_name  = ""
        self._assert_club_is_invalid()

    def test_club_name_must_be_unique(self):
        second_club = _create_second_club()
        second_club.club_name = self.club.club_name
        self._assert_club_is_invalid()

    def test_club_name_can_be_50_characters(self):
        self.club.club_name = "x" * 50
        self._assert_club_is_valid()

    def test_club_name_cannot_be_51_characters(self):
        self.club.club_name = "x" * 51
        self._assert_club_is_invalid()


    """Tests for club_codename field"""
    def test_codename_generates_correctly(self):
        self.assertEqual(helpers.convert_to_codename(self.club.club_name), self.club.club_codename)

    def test_club_codename_cannot_be_blank(self):
        self.club.club_codename = ""
        self._assert_club_is_invalid()

    def test_club_codename_must_be_unique(self):
        second_club = _create_second_club()
        second_club.club_name = self.club.club_name
        self._assert_club_is_invalid()

    def test_club_codename_can_be_50_characters(self):
        self.club.club_name = "x" * 50
        self._assert_club_is_valid()

    def test_club_codename_cannot_be_51_characters(self):
        self.club.club_name = "x" * 51
        self._assert_club_is_invalid()


    """Tests for mission_statement field"""
    def test_club_mission_statement_can_be_blank(self):
        self.club.mission_statement = ""
        self._assert_club_is_valid()

    def test_club_mission_statement_need_not_be_unique(self):
        second_club = _create_second_club()
        second_club.mission_statement = self.club.mission_statement
        self._assert_club_is_valid()

    def test_club_mission_statement_can_be_150_characters(self):
        self.club.club_name = "x" * 150
        self._assert_club_is_valid()

    def test_club_mission_statement_cannot_be_151_characters(self):
        self.club.club_name = "x" * 151
        self._assert_club_is_invalid()


    """Tests for member_count field"""

    def _assert_club_is_valid(self):
        try:
            self.club.full_clean()
        except(ValidationError):
            self.fail("Test club should be valid")

    def _assert_club_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.club.full_clean()
