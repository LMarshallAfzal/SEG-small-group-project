"""Unit tests of the Club model"""
from django.test import TestCase
from clubs.models import Club
from django.core.exceptions import ValidationError
import clubs.helpers

class ClubModelTestCase(TestCase):
    """Unit tests of the Club model"""
    def setUp(self):
        name = "Generic chess club"
        mission_statement = "Play chess here"
        location = "40 Aldwych\nLondon, WC2B 4BG"
        self.club = Club.objects.create_club(name, mission_statement, location)
