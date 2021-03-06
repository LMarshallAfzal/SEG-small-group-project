"""Test of the officer view"""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club
from django.contrib.auth.models import Group
from clubs.club_list import ClubList

class UserFormTestCase(TestCase):
    """Unit tests of the user form."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_user.json',
        'clubs/tests/fixtures/member.json',
        'clubs/tests/fixtures/applicant.json',
    ]


    def setUp(self):
        list_of_clubs = ClubList()
        self.club = list_of_clubs.create_new_club("Cambridge Chessinators", "Cambridge > Oxford", "Cambridge")


        self.user = User.objects.get(email = "johndoe@example.org")
        self.url = reverse('owner')
        self.officer_user = User.objects.get(email = 'janedoe@example.org')
        self.member_user = User.objects.get(email = 'petrapickles@example.org')
        self.applicant_user = User.objects.get(email = 'peterpickles@example.org')

        self.owner = Group.objects.get(name = self.club.getClubOwnerGroup())
        self.club.add_user_to_club(self.user, "Owner")

        self.officer = Group.objects.get(name = self.club.getClubOfficerGroup())
        self.club.add_user_to_club(self.officer_user, "Officer")

        self.member = Group.objects.get(name = self.club.getClubMemberGroup())
        self.club.add_user_to_club(self.member_user, "Member")

        self.applicant = Group.objects.get(name = self.club.getClubApplicantGroup())
        self.club.add_user_to_club(self.applicant_user,"Applicant")



    def test_owner_url(self):
        self.assertEqual(self.url,'/owner/')

    def test_get_owner_view(self):
        self.client.login(email=self.user.email, password='Password123')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'owner.html')

    def test_promote_member_to_officer(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self.member_user.groups.filter(name = self.club.getClubMemberGroup()).exists())
        self.assertFalse(self.member_user.groups.filter(name = self.club.getClubOfficerGroup()).exists())
        self.officer.user_set.add(self.member_user)
        self.member.user_set.remove(self.member_user)
        self.assertTrue(self.member_user.groups.filter(name = self.club.getClubOfficerGroup()).exists())
        self.assertFalse(self.member_user.groups.filter(name = self.club.getClubMemberGroup()).exists())

    def test_officer_can_be_demoted(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self.officer_user.groups.filter(name = self.club.getClubOfficerGroup()).exists())
        self.officer.user_set.remove(self.officer_user)
        self.member.user_set.add(self.officer_user)
        self.assertFalse(self.officer_user.groups.filter(name = self.club.getClubOfficerGroup()).exists())
        self.assertTrue(self.officer_user.groups.filter(name =self.club.getClubMemberGroup()).exists())


    def test_cannnot_promote_member_to_owner(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertFalse(self.member_user.groups.filter(name = self.club.getClubOfficerGroup()).exists())
        self.assertTrue(self.member_user.groups.filter(name = self.club.getClubMemberGroup()).exists())
        self.owner.user_set.add(self.member_user)
        self.assertFalse(self.member_user.groups.filter(name= self.club.getClubOwnerGroup).exists())
        self.assertFalse(self.member_user.groups.filter(name = self.club.getClubOfficerGroup()).exists())


    def test_officer_can_be_promoted(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self.officer_user.groups.filter(name = self.club.getClubOfficerGroup()).exists())
        self.owner.user_set.add(self.officer_user)
        self.assertTrue(self.user.groups.filter(name=self.club.getClubOwnerGroup()).exists())
