"""Unit tests of the Club model as well as the groups created by the club"""
from django.test import TestCase
from clubs.models import Club, User
from django.core.exceptions import ValidationError
import clubs.helpers as h
from django.contrib.auth.models import Group

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
        second_club = Club.objects.create_club(
            name = "Even more generic chess club",
            mission_statement = "Play chess",
            location = "Somewhere"
        )
        return second_club

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
        second_club = self._create_second_club()
        self.club.club_name = second_club.club_name
        self._assert_club_is_invalid()

    def test_club_name_can_be_50_characters(self):
        self.club.club_name = "x" * 50
        self._assert_club_is_valid()

    def test_club_name_cannot_be_51_characters(self):
        self.club.club_name = "x" * 51
        self._assert_club_is_invalid()


    """Tests for club_codename field"""
    def test_codename_generates_correctly(self):
        self.assertEqual(h.convert_to_codename(self.club.club_name), self.club.club_codename)

    def test_club_codename_cannot_be_blank(self):
        self.club.club_codename = ""
        self._assert_club_is_invalid()

    def test_club_codename_must_be_unique(self):
        second_club = self._create_second_club()
        self.club.club_name = second_club.club_name
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
        second_club = self._create_second_club()
        second_club.mission_statement = self.club.mission_statement
        self._assert_club_is_valid()

    def test_club_mission_statement_can_be_150_characters(self):
        self.club.mission_statement = "x" * 150
        self._assert_club_is_valid()

    def test_club_mission_statement_cannot_be_151_characters(self):
        self.club.mission_statement = "x" * 151
        self._assert_club_is_invalid()


    """Tests for club_location field"""
    def test_location_can_be_blank(self):
        self.club.club_location = ""
        self._assert_club_is_valid()

    def test_location_need_not_be_unique(self):
        second_club = self._create_second_club()
        self.club_club_location = second_club.club_location
        self._assert_club_is_valid()

    def test_location_can_be_100_characters(self):
        self.club.club_location = "x" * 100
        self._assert_club_is_valid()

    def test_club_location_cannot_be_101_characters(self):
        self.club.club_location = "x" * 101
        self._assert_club_is_invalid()


    """Tests for member_count field"""
    def test_member_count_starts_at_zero(self):
        self.assertEqual(self.club.member_count, 0)

    def test_member_count_increments_when_adding_a_member(self):
        user = self._create_new_user()
        count = self.club.member_count
        self.club.add_user_to_club(user, "Member")
        self.assertEqual(count+1, self.club.member_count)

    def test_member_count_does_not_increment_when_adding_an_applicant(self):
        user = self._create_new_user()
        count = self.club.member_count
        self.club.add_user_to_club(user, "Applicant")
        self.assertEqual(count, self.club.member_count)

    def test_member_count_does_not_increment_when_adding_an_officer(self):
        user = self._create_new_user()
        count = self.club.member_count
        self.club.add_user_to_club(user, "Officer")
        self.assertEqual(count, self.club.member_count)

    def test_member_count_does_not_increment_when_adding_an_owner(self):
        user = self._create_new_user()
        count = self.club.member_count
        self.club.add_user_to_club(user, "Owner")
        self.assertEqual(count, self.club.member_count)

    def test_member_count_increments_when_switching_user_role_to_member(self):
        user = self._create_new_user()
        self.club.add_user_to_club(user, "Applicant")
        count = self.club.member_count
        self.club.switch_user_role_in_club(user, "Member")
        self.assertEqual(count+1, self.club.member_count)

    def test_member_count_does_not_increment_when_switching_user_role_to_non_member(self):
        user = self._create_new_user()
        self.club.add_user_to_club(user, "Applicant")
        count = self.club.member_count
        self.club.switch_user_role_in_club(user, "Officer")
        self.assertEqual(count, self.club.member_count)

    def test_member_count_decrements_when_switching_user_role_from_member(self):
        user = self._create_new_user()
        self.club.add_user_to_club(user, "Member")
        count = self.club.member_count
        self.club.switch_user_role_in_club(user, "Officer")
        self.assertEqual(count-1, self.club.member_count)

    def test_member_count_decrements_when_removing_member_from_club(self):
        user = self._create_new_user()
        self.club.add_user_to_club(user, "Member")
        count = self.club.member_count
        self.club.remove_user_from_club(user)
        self.assertEqual(count-1, self.club.member_count)

    def test_member_count_does_not_decrement_when_removing_applicant_from_club(self):
        user = self._create_new_user()
        self.club.add_user_to_club(user, "Applicant")
        count = self.club.member_count
        self.club.remove_user_from_club(user)
        self.assertEqual(count, self.club.member_count)

    def test_member_count_does_not_decrement_when_removing_officer_from_club(self):
        user = self._create_new_user()
        self.club.add_user_to_club(user, "Officer")
        count = self.club.member_count
        self.club.remove_user_from_club(user)
        self.assertEqual(count, self.club.member_count)

    def test_member_count_does_not_decrement_when_removing_owner_from_club(self):
        user = self._create_new_user()
        self.club.add_user_to_club(user, "Owner")
        count = self.club.member_count
        self.club.remove_user_from_club(user)
        self.assertEqual(count, self.club.member_count)

    def test_attempting_to_remove_user_who_is_not_part_of_a_club_does_not_reduce_member_count(self):
        user = self._create_new_user()
        count = self.club.member_count
        self.club.remove_user_from_club(user)
        self.assertEqual(count, self.club.member_count)

    def test_adding_a_user_to_multiple_clubs_as_a_member_increments_member_count_correctly_for_both_clubs(self):
        user = self._create_new_user()
        second_club = self._create_second_club()
        first_club_member_count = self.club.member_count
        second_club_member_count = second_club.member_count
        self.club.add_user_to_club(user, "Member")
        second_club.add_user_to_club(user, "Member")
        self.assertEqual(first_club_member_count+1, self.club.member_count)
        self.assertEqual(second_club_member_count+1, second_club.member_count)

    def test_adding_a_user_to_multiple_clubs_as_a_member_for_only_one_of_them_increments_member_count_correctly_for_both_clubs(self):
        user = self._create_new_user()
        second_club = self._create_second_club()
        first_club_member_count = self.club.member_count
        second_club_member_count = second_club.member_count
        self.club.add_user_to_club(user, "Member")
        second_club.add_user_to_club(user, "Applicant")
        self.assertEqual(first_club_member_count+1, self.club.member_count)
        self.assertEqual(second_club_member_count, second_club.member_count)

    def test_adding_a_user_to_multiple_clubs_as_a_non_member_for_both_does_not_increment_either_member_count(self):
        user = self._create_new_user()
        second_club = self._create_second_club()
        first_club_member_count = self.club.member_count
        second_club_member_count = second_club.member_count
        self.club.add_user_to_club(user, "Applicant")
        second_club.add_user_to_club(user, "Applicant")
        self.assertEqual(first_club_member_count, self.club.member_count)
        self.assertEqual(second_club_member_count, second_club.member_count)

    def test_switching_a_user_to_member_in_one_club_does_not_affect_member_count_for_the_other(self):
        user = self._create_new_user()
        second_club = self._create_second_club()
        first_club_member_count = self.club.member_count
        second_club_member_count = second_club.member_count
        self.club.add_user_to_club(user, "Applicant")
        second_club.add_user_to_club(user, "Applicant")
        first_club_member_count = self.club.member_count
        second_club_member_count = second_club.member_count
        self.club.switch_user_role_in_club(user, "Member")
        self.assertEqual(first_club_member_count+1, self.club.member_count)
        self.assertEqual(second_club_member_count, second_club.member_count)

    def test_switching_a_user_from_member_in_one_club_does_not_affect_member_count_for_the_other(self):
        user = self._create_new_user()
        second_club = self._create_second_club()
        first_club_member_count = self.club.member_count
        second_club_member_count = second_club.member_count
        self.club.add_user_to_club(user, "Member")
        second_club.add_user_to_club(user, "Applicant")
        first_club_member_count = self.club.member_count
        second_club_member_count = second_club.member_count
        self.club.switch_user_role_in_club(user, "Officer")
        self.assertEqual(first_club_member_count-1, self.club.member_count)
        self.assertEqual(second_club_member_count, second_club.member_count)


    """Tests around the groups automatically created by the club"""
    def test_club_automatically_generates_applicant_group_for_club(self):
        applicant_group = self.club.getClubApplicantGroup()
        self.assertEqual(applicant_group, Group.objects.get(self.club.club_codename + " Applicant"))

    def test_club_automatically_generates_member_group_for_club(self):
        member_group = self.club.getClubMemberGroup()
        self.assertEqual(member_group, Group.objects.get(self.club.club_codename + " Member"))

    def test_club_automatically_generates_officer_group_for_club(self):
        officer_group = self.club.getClubOfficerGroup()
        self.assertEqual(officer_group, Group.objects.get(self.club.club_codename + " Officer"))

    def test_club_automatically_generates_owner_group_for_club(self):
        owner_group = self.club.getClubOwnerGroup()
        self.assertEqual(owner_group, Group.objects.get(self.club.club_codename + " Owner"))

    def test_switching_user_roles_in_a_club_means_the_user_is_not_part_of_the_old_role(self):
        user = self._create_new_user()
        self.club.add_user_to_club(user, "Applicant")
        self.club.switch_user_role_in_club(user, "Member")
        self.assertFalse(user.groups.filter(name = self.club.club_codename + " Applicant").exists())
        self.assertTrue(user.groups.filter(name = self.club.club_codename + " Member").exists())

    def test_attempting_to_switch_user_roles_in_a_club_they_are_not_a_part_off_does_not_add_them_to_the_club(self):
        user = self._create_new_user()
        self.club.switch_user_role_in_club(user, "Member")
        self.assertFalse(user.groups.filter(name = self.club.club_codename + " Member").exists())

    def test_removing_a_user_from_the_club_removes_them_from_the_relevant_groups(self):
        pass

    def test_attempting_to_remove_a_user_from_a_club_they_are_not_a_part_of_does_nothing(self):
        pass


    def _assert_club_is_valid(self):
        try:
            self.club.full_clean()
        except(ValidationError):
            self.fail("Test club should be valid")

    def _assert_club_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.club.full_clean()
