"""Tests of the ClubList class and the multi-class functionality it helps to provide"""
from django.test import TestCase
from clubs.models import Club, User
from clubs.club_list import ClubList
from django.core.exceptions import ValidationError
import clubs.helpers
from faker import Faker
import faker.providers

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

    #Uses random user creation from seed command
    def _create_random_user(self):
        new_faker = Faker('en_GB')
        firstName = self.faker.unique.first_name()
        lastName = self.faker.unique.last_name()
        email1 = f'{firstName}.{lastName}@example.org'
        userName = email1
        pass1 = "Password123"
        bio1 = self.faker.unique.text(max_nb_chars = 520)
        personalStatement = self.faker.text(max_nb_chars=1250)

        new_user = User.objects.create_user(
            username = userName,
            first_name = firstName,
            last_name = lastName,
            email = email1,
            password = pass1,
            bio = bio1,
            personal_statement = personalStatement,
        )
        return new_user


    def _test_club_list_starts_with_0_entries(self):
