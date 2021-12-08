"""Unit tests of the Club model"""
from django.test import TestCase
from clubs.models import Club
from django.core.exceptions import ValidationError
import clubs.helpers

class ClubModelTestCase(TestCase):
    """Unit tests of the Club model"""
    def setUp(self):
        name = "Generic chess club"
        self.club = Club.objects.create_club(name)
