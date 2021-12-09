"""Unit tests of the User model"""
from django.test import TestCase
from clubs.models import Club
from django.core.exceptions import ValidationError

class ClubModelTestCase(TestCase):
    """Unit tests of the User model"""
    def setUp(self):
        self.club = Club.objects.create_club("Test club", "Test mission statement"
        )

    def test_club_name_must_not_be_blank(self):
        self.club.club_name = ''
        self._assert_club_is_invalid()

    def test_club_name_can_be_50_characters_long(self):
        self.club.club_name = 'x' *50
        self._assert_club_is_valid()

    def test_club_name_can_not_be_longer_50_characters_long(self):
        self.club.club_name = 'x' *51
        self._assert_club_is_invalid()

    def test_mission_statement_can_be_50_characters_long(self):
        self.club.mission_statement = 'x' *150
        self._assert_club_is_valid()

    def test_mission_statement_can_not_be_longer_150_characters_long(self):
        self.club.mission_statement = 'x' *151
        self._assert_club_is_invalid()

    def _create_second_club(self):
        club = Club.objects.create_club("Test2 club", "Test2 mission statement")
        return club

    def _assert_club_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.club.full_clean()

    def _assert_club_is_valid(self):
        try:
            self.club.full_clean()
        except(ValidationError):
            self.fail('Test club should be valid')
