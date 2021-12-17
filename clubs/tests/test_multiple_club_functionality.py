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
        return self.list_of_clubs.create_new_club("Test chess club", "Play chess here", "London")

    def _create_second_club(self):
        return self.list_of_clubs.create_new_club("Other chess club", "Play chess", "England")

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
        found_club = self._create_club()
        self.assertTrue(isinstance(found_club, Club))

    def test_find_club_returns_correct_club_object(self):
        found_club = self._create_club()
        self.assertEqual(found_club.club_name, "Test chess club")

    def test_find_club_returns_correct_club_object_from_multiple(self):
        self._create_club()
        found_club = self._create_second_club()
        self.assertEqual(found_club.club_name, "Other chess club")

    def test_find_club_returns_None_when_finding_club_that_does_not_exist(self):
        self._create_club()
        found_club = self.list_of_clubs.find_club("Other chess club")
        self.assertEqual(found_club, None)

    def test_find_club_returns_None_if_list_is_empty(self):
        found_club = self.list_of_clubs.find_club("Test chess club")
        self.assertEqual(found_club, None)

    def test_find_club_returns_correct_club_even_when_using_club_codename(self):
        club_to_find = self._create_club()
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


    """Tests for the get_all_clubs() function"""
    def test_get_all_clubs_correctly_gets_every_club(self):
        first_club = self._create_club()
        second_club = self._create_second_club()
        expected_clubs = [first_club, second_club]
        all_clubs = self.list_of_clubs.get_all_clubs()
        self.assertEqual(len(expected_clubs), len(all_clubs))
        for i in range(len(all_clubs)):
            self.assertEqual(all_clubs[i], expected_clubs[i])

    def test_get_all_clubs_correctly_gets_one_club_if_there_is_only_one_club(self):
        club = self._create_club()
        all_clubs = self.list_of_clubs.get_all_clubs()
        self.assertEqual(len(all_clubs), 1)
        self.assertEqual(all_clubs[0], club)

    def test_get_all_clubs_returns_an_empty_list_if_there_are_no_clubs(self):
        all_clubs = self.list_of_clubs.get_all_clubs()
        self.assertEqual(len(all_clubs), 0)


    """Tests for the get_all_groups() function"""
    def test_get_all_groups_correctly_returns_every_group_for_every_club(self):
        first_club = self._create_club()
        second_club = self._create_second_club()
        all_groups = self.list_of_clubs.get_all_groups()
        expected_groups = [
            [
                Group.objects.get(name = first_club.club_codename + " Applicant"),
                Group.objects.get(name = first_club.club_codename + " Member"),
                Group.objects.get(name = first_club.club_codename + " Officer"),
                Group.objects.get(name = first_club.club_codename + " Owner")
            ],
            [
                Group.objects.get(name = second_club.club_codename + " Applicant"),
                Group.objects.get(name = second_club.club_codename + " Member"),
                Group.objects.get(name = second_club.club_codename + " Officer"),
                Group.objects.get(name = second_club.club_codename + " Owner")
            ]
        ]
        self.assertEqual(len(all_groups), len(expected_groups))
        for i in range(len(all_groups)):
            self.assertEqual(all_groups[i], expected_groups[i])

    def test_get_all_groups_returns_a_2D_list_even_with_only_1_club(self):
        first_club = self._create_club()
        all_groups = self.list_of_clubs.get_all_groups()
        expected_groups = [
            [
                Group.objects.get(name = first_club.club_codename + " Applicant"),
                Group.objects.get(name = first_club.club_codename + " Member"),
                Group.objects.get(name = first_club.club_codename + " Officer"),
                Group.objects.get(name = first_club.club_codename + " Owner")
            ]
        ]
        self.assertEqual(len(all_groups), 1)
        self.assertEqual(all_groups[0], expected_groups[0])

    def test_get_all_groups_returns_an_empty_list_if_there_are_no_clubs(self):
        all_groups = self.list_of_clubs.get_all_groups()
        self.assertEqual(len(all_groups), 0)


    """Tests for users interacting with multiple clubs"""
    def test_users_can_be_a_part_of_multiple_clubs_with_the_same_role(self):
        user = self._create_random_user()
        first_club = self._create_club()
        second_club = self._create_second_club()
        first_club.add_user_to_club(user, "Applicant")
        second_club.add_user_to_club(user, "Applicant")
        self.assertEqual(user.groups.all().count(), 2)
        self.assertTrue(user.groups.filter(name = first_club.club_codename + " Applicant").exists())
        self.assertTrue(user.groups.filter(name = second_club.club_codename + " Applicant").exists())

    def test_users_can_be_a_part_of_multiple_clubs_with_different_roles(self):
        user = self._create_random_user()
        first_club = self._create_club()
        second_club = self._create_second_club()
        first_club.add_user_to_club(user, "Applicant")
        second_club.add_user_to_club(user, "Member")
        self.assertEqual(user.groups.all().count(), 2)
        self.assertTrue(user.groups.filter(name = first_club.club_codename + " Applicant").exists())
        self.assertTrue(user.groups.filter(name = second_club.club_codename + " Member").exists())

    def test_switching_the_role_of_a_user_in_a_club_does_not_affect_the_other_club(self):
        user = self._create_random_user()
        first_club = self._create_club()
        second_club = self._create_second_club()
        first_club.add_user_to_club(user, "Applicant")
        second_club.add_user_to_club(user, "Applicant")
        first_club.switch_user_role_in_club(user, "Member")
        self.assertEqual(user.groups.all().count(), 2)
        self.assertTrue(user.groups.filter(name = first_club.club_codename + " Member").exists())
        self.assertFalse(user.groups.filter(name = first_club.club_codename + " Applicant").exists())
        self.assertTrue(user.groups.filter(name = second_club.club_codename + " Applicant").exists())

    def test_deleting_a_user_from_a_club_does_not_affect_the_other_club(self):
        user = self._create_random_user()
        first_club = self._create_club()
        second_club = self._create_second_club()
        first_club.add_user_to_club(user, "Applicant")
        second_club.add_user_to_club(user, "Applicant")
        first_club.remove_user_from_club(user)
        self.assertFalse(user.groups.filter(name = first_club.club_codename + " Applicant").exists())
        self.assertTrue(user.groups.filter(name = second_club.club_codename + " Applicant").exists())


    """Tests for the get_user_clubs() function"""
    def test_get_user_clubs_returns_club_objects(self):
        user = self._create_random_user()
        first_club = self._create_club()
        second_club = self._create_second_club()
        first_club.add_user_to_club(user, "Applicant")
        second_club.add_user_to_club(user, "Applicant")
        user_clubs = self.list_of_clubs.get_user_clubs(user)
        expected_clubs = [first_club, second_club] #The order of clubs does not need to be fixed, but in most cases will be in the order they were created
        self.assertEqual(len(user_clubs), len(expected_clubs))
        for i in range(len(user_clubs)):
            self.assertTrue(user_clubs[i] in expected_clubs)

    def test_get_user_clubs_returns_a_single_club_if_the_user_is_only_a_part_of_one_club(self):
        user = self._create_random_user()
        first_club = self._create_club()
        first_club.add_user_to_club(user, "Applicant")
        user_clubs = self.list_of_clubs.get_user_clubs(user)
        self.assertEqual(len(user_clubs), 1)
        self.assertEqual(user_clubs[0], first_club)

    def test_get_user_clubs_returns_clubs_that_a_user_is_a_part_of_not_just_every_club(self):
        user = self._create_random_user()
        first_club = self._create_club()
        second_club = self._create_second_club()
        first_club.add_user_to_club(user, "Applicant")
        user_clubs = self.list_of_clubs.get_user_clubs(user)
        self.assertEqual(len(user_clubs), 1)
        self.assertFalse(second_club in user_clubs)
        self.assertEqual(user_clubs[0], first_club)

    def test_get_user_clubs_returns_clubs_user_is_an_applicant_of(self):
        user = self._create_random_user()
        first_club = self._create_club()
        first_club.add_user_to_club(user, "Applicant")
        user_clubs = self.list_of_clubs.get_user_clubs(user)
        self.assertEqual(len(user_clubs), 1)
        self.assertEqual(user_clubs[0], first_club)

    def test_get_user_clubs_returns_clubs_user_is_a_member_of(self):
        user = self._create_random_user()
        first_club = self._create_club()
        first_club.add_user_to_club(user, "Member")
        user_clubs = self.list_of_clubs.get_user_clubs(user)
        self.assertEqual(len(user_clubs), 1)
        self.assertEqual(user_clubs[0], first_club)

    def test_get_user_clubs_returns_clubs_user_is_an_officer_of(self):
        user = self._create_random_user()
        first_club = self._create_club()
        first_club.add_user_to_club(user, "Officer")
        user_clubs = self.list_of_clubs.get_user_clubs(user)
        self.assertEqual(len(user_clubs), 1)
        self.assertEqual(user_clubs[0], first_club)

    def test_get_user_clubs_returns_clubs_user_is_an_owner_of(self):
        user = self._create_random_user()
        first_club = self._create_club()
        first_club.add_user_to_club(user, "Owner")
        user_clubs = self.list_of_clubs.get_user_clubs(user)
        self.assertEqual(len(user_clubs), 1)
        self.assertEqual(user_clubs[0], first_club)

    def test_get_user_clubs_returns_an_empty_list_if_there_are_no_clubs_the_user_is_a_part_of(self):
        user = self._create_random_user()
        self._create_club()
        user_clubs = self.list_of_clubs.get_user_clubs(user)
        self.assertEqual(len(user_clubs), 0)

    def test_get_user_clubs_returns_clubs_for_inputted_user_not_just_all_users(self):
        user1 = self._create_random_user()
        user2 = self._create_random_user()
        first_club = self._create_club()
        second_club = self._create_second_club()
        first_club.add_user_to_club(user1, "Applicant")
        second_club.add_user_to_club(user2, "Applicant")
        user1_clubs = self.list_of_clubs.get_user_clubs(user1)
        user2_clubs = self.list_of_clubs.get_user_clubs(user2)
        self.assertEqual(len(user1_clubs), 1)
        self.assertEqual(len(user2_clubs), 1)
        self.assertEqual(user1_clubs[0], first_club)
        self.assertEqual(user2_clubs[0], second_club)
