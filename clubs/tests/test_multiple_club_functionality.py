"""Tests of the ClubList class and the multi-club functionality it helps to provide"""
from django.test import TestCase
from clubs.models import Club, User
from clubs.club_list import ClubList
from django.core.exceptions import ValidationError
import clubs.helpers
from faker import Faker
import faker.providers
import clubs.helpers as h

class ClubListTestCase(TestCase):
    """Tests of the ClubList class and the multi-club functionality it helps to provide"""
    def setUp(self):
        self.list_of_clubs = ClubList()

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
        self.assertEqual(len(self.list_of_clubs.club_list), 0)

    """Tests for the create_new_club() function"""
    def test_adding_a_club_increments_number_of_entries(self):
        number_of_clubs = len(self.list_of_clubs.club_list)
        self.list_of_clubs.create_new_club("Test chess club", "Play chess here", "London")
        self.assertEqual(number_of_clubs+1, len(self.list_of_clubs.club_list))

    def test_adding_2_clubs_increments_number_of_entries_by_two(self):
        number_of_clubs = len(self.list_of_clubs.club_list)
        self.list_of_clubs.create_new_club("Test chess club", "Play chess here", "London")
        self.list_of_clubs.create_new_club("Other chess club", "Play chess", "England")
        self.assertEqual(number_of_clubs+2, len(self.list_of_clubs.club_list))

    def test_adding_2_clubs_with_the_same_name_only_increments_number_of_entries_by_one(self):
        number_of_clubs = len(self.list_of_clubs.club_list)
        self.list_of_clubs.create_new_club("Test chess club", "Play chess here", "London")
        self.list_of_clubs.create_new_club("Test chess club", "Play chess", "England")
        self.assertEqual(number_of_clubs+1, len(self.list_of_clubs.club_list))


    """Tests for the find_club() function"""
    def test_find_club_returns_a_club_object(self):
        self.list_of_clubs.create_new_club("Test chess club", "Play chess here", "London")
        found_club = self.list_of_clubs.find_club("Test chess club")
        self.assertTrue(isinstance(found_club, Club))

    def test_find_club_returns_correct_club_object(self):
        self.list_of_clubs.create_new_club("Test chess club", "Play chess here", "London")
        found_club = self.list_of_clubs.find_club("Test chess club")
        self.assertEqual(found_club, Club.objects.get(name = "Test chess club"))

    def test_find_club_returns_correct_club_object_from_multiple(self):
        self.list_of_clubs.create_new_club("Test chess club", "Play chess here", "London")
        self.list_of_clubs.create_new_club("Other chess club", "Play chess", "England")
        found_club = self.list_of_clubs.find_club("Other chess club")
        self.assertEqual(found_club, Club.objects.get(name = "Other chess club"))

    def test_find_club_returns_None_when_finding_club_that_does_not_exist(self):
        self.list_of_clubs.create_new_club("Test chess club", "Play chess here", "London")
        found_club = self.list_of_clubs.find_club("Other chess club")
        self.assertEqual(found_club, None)

    def test_find_club_returns_None_if_list_is_empty(self):
        found_club = self.list_of_clubs.find_club("Test chess club")
        self.assertEqual(found_club, None)


    """Tests for the delete_club() function"""
    def test_deleting_a_club_decrements_number_of_entries(self):
        self.list_of_clubs.create_club("Test chess club", "Play chess here", "London")
        number_of_clubs = len(self.list_of_clubs.club_list)
        club_to_delete = self.list_of_clubs.find_club("Test chess club")
        self.list_of_clubs.delete_club(club_to_delete)
        self.assertEqual(number_of_clubs-1, len(self.list_of_clubs.club_list))
