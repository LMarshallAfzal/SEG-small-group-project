"""Tests of the ClubList class and the multi-class functionality it helps to provide"""
from django.test import TestCase
from clubs.models import Club, User
from clubs.club_list import ClubList
from django.core.exceptions import ValidationError
import clubs.helpers
from faker import Faker

class ClubListTestCase(TestCase):
    """Tests of the ClubList class and the multi-class functionality it helps to provide"""
    def setUp(self):
        self.list_of_clubs = ClubList()

    def _create_random_club(self):
        new_faker = Faker('en_GB')
        new_club = self.list_of_clubs.create_club(
            new_faker.unique.text(max_nb_chars = 50),
            new_faker.unique.text(max_nb_chars = 150),
            new_faker.unique.text(max_nb_chars = 100)
        )
        return new_club
