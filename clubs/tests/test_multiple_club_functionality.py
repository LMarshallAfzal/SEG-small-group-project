"""Tests of the ClubList class and the multi-club functionality it helps to provide"""
from django.test import TestCase
from clubs.models import Club, User
from clubs.club_list import ClubList
from django.core.exceptions import ValidationError
import clubs.helpers
from faker import Faker
import faker.providers
import clubs.helpers as h
from django.contrib.auth.models import Group

class ClubListTestCase(TestCase):
    """Tests of the ClubList class and the multi-club functionality it helps to provide"""
    def setUp(self):
        self.list_of_clubs = ClubList()

    def _create_club(self):
        self.list_of_clubs.create_new_club("Test chess club", "Play chess here", "London")

    def _create_and_find_club(self):
        self.list_of_clubs.create_new_club("Test chess club", "Play chess here", "London")
        return self.list_of_clubs.find_club("Test chess club")

    def _create_second_club(self):
        self.list_of_clubs.create_new_club("Other chess club", "Play chess", "England")

    def _create_and_find_second_club(self):
        self.list_of_clubs.create_new_club("Other chess club", "Play chess", "England")
        return self.list_of_clubs.find_club("Other chess club")

    #Uses random user creation from seed command
    def _create_random_user(self):
        new_faker = Faker('en_GB')
        firstName = new_faker.unique.first_name()
        lastName = new_faker.unique.last_name()
        email1 = f'{firstName}.{lastName}@example.org'
        userName = email1
        pass1 = "Password123"
        bio1 = new_faker.unique.text(max_nb_chars = 520)
        personalStatement = new_faker.text(max_nb_chars=1250)

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
        self._create_club()
        self.assertEqual(number_of_clubs+1, len(self.list_of_clubs.club_list))

    def test_adding_2_clubs_increments_number_of_entries_by_two(self):
        number_of_clubs = len(self.list_of_clubs.club_list)
        self._create_club()
        self._create_second_club()
        self.assertEqual(number_of_clubs+2, len(self.list_of_clubs.club_list))

    def test_adding_2_clubs_with_the_same_name_only_increments_number_of_entries_by_one(self):
        number_of_clubs = len(self.list_of_clubs.club_list)
        self._create_club()
        self._create_club()
        self.assertEqual(number_of_clubs+1, len(self.list_of_clubs.club_list))


    """Tests for the find_club() function"""
    def test_find_club_returns_a_club_object(self):
        found_club = self._create_and_find_club()
        self.assertTrue(isinstance(found_club, Club))

    def test_find_club_returns_correct_club_object(self):
        found_club = self._create_and_find_club()
        self.assertEqual(found_club.club_name, "Test chess club")

    def test_find_club_returns_correct_club_object_from_multiple(self):
        self._create_club()
        found_club = self._create_and_find_second_club()
        self.assertEqual(found_club.club_name, "Other chess club")

    def test_find_club_returns_None_when_finding_club_that_does_not_exist(self):
        self._create_club()
        found_club = self.list_of_clubs.find_club("Other chess club")
        self.assertEqual(found_club, None)

    def test_find_club_returns_None_if_list_is_empty(self):
        found_club = self.list_of_clubs.find_club("Test chess club")
        self.assertEqual(found_club, None)

    def test_find_club_returns_correct_club_even_when_using_club_codename(self):
        club_to_find = self._create_and_find_club()
        found_club = self.list_of_clubs.find_club(h.convert_to_codename(club_to_find.club_name))
        self.assertEqual(club_to_find, found_club)


    """Tests for the delete_club() function"""
    def test_deleting_a_club_decrements_number_of_entries(self):
        self._create_club()
        number_of_clubs = len(self.list_of_clubs.club_list)
        self.list_of_clubs.delete_club("Test chess club")
        self.assertEqual(number_of_clubs-1, len(self.list_of_clubs.club_list))

    def test_attempting_to_delete_a_club_when_none_exist_does_not_decrement_number_of_entries(self):
        number_of_clubs = len(self.list_of_clubs.club_list)
        self.list_of_clubs.delete_club("Test chess club")
        self.assertEqual(number_of_clubs, len(self.list_of_clubs.club_list))

    def test_deleting_a_club_that_does_not_exist_does_not_decrement_number_of_entries(self):
        self._create_club()
        number_of_clubs = len(self.list_of_clubs.club_list)
        self.list_of_clubs.delete_club("Other chess club")
        self.assertEqual(number_of_clubs, len(self.list_of_clubs.club_list))

    def test_deleting_a_club_does_not_delete_multiple_from_the_list(self):
        self._create_club()
        self._create_second_club()
        number_of_clubs = len(self.list_of_clubs.club_list)
        self.list_of_clubs.delete_club("Test chess club")
        self.assertEqual(number_of_clubs-1, len(self.list_of_clubs.club_list))

    def test_attempting_to_delete_the_same_club_twice_only_removes_a_club_once(self):
        self._create_club()
        number_of_clubs = len(self.list_of_clubs.club_list)
        self.list_of_clubs.delete_club("Test chess club")
        self.list_of_clubs.delete_club("Test chess club")
        self.assertEqual(number_of_clubs-1, len(self.list_of_clubs.club_list))


    """Tests for users interacting with multiple clubs"""
    def test_users_can_be_a_part_of_multiple_clubs_with_the_same_role(self):
        user = self._create_random_user()
        first_club = self._create_and_find_club()
        second_club = self._create_and_find_second_club()
        first_club.add_user_to_club(user, "Applicant")
        second_club.add_user_to_club(user, "Applicant")
        self.assertEquals(user.groups.all().count(), 2)
        self.assertTrue(user.groups.filter(name = first_club.club_codename + " Applicant").exists())
        self.assertTrue(user.groups.filter(name = second_club.club_codename + " Applicant").exists())

    def test_users_can_be_a_part_of_multiple_clubs_with_different_roles(self):
        user = self._create_random_user()
        first_club = self._create_and_find_club()
        second_club = self._create_and_find_second_club()
        first_club.add_user_to_club(user, "Applicant")
        second_club.add_user_to_club(user, "Member")
        self.assertEquals(user.groups.all().count(), 2)
        self.assertTrue(user.groups.filter(name = first_club.club_codename + " Applicant").exists())
        self.assertTrue(user.groups.filter(name = second_club.club_codename + " Member").exists())

    def test_switching_the_role_of_a_user_in_a_club_does_not_affect_the_other_club(self):
        user = self._create_random_user()
        first_club = self._create_and_find_club()
        second_club = self._create_and_find_second_club()
        first_club.add_user_to_club(user, "Applicant")
        second_club.add_user_to_club(user, "Applicant")
        first_club.switch_user_role_in_club(user, "Member")
        self.assertEquals(user.groups.all().count(), 2)
        self.assertTrue(user.groups.filter(name = first_club.club_codename + " Member").exists())
        self.assertFalse(user.groups.filter(name = first_club.club_codename + " Applicant").exists())
        self.assertTrue(user.groups.filter(name = second_club.club_codename + " Applicant").exists())

    def test_deleting_a_user_from_a_club_does_not_affect_the_other_club(self):
        user = self._create_random_user()
        first_club = self._create_and_find_club()
        second_club = self._create_and_find_second_club()
        first_club.add_user_to_club(user, "Applicant")
        second_club.add_user_to_club(user, "Applicant")
        first_club.remove_user_from_club(user)
