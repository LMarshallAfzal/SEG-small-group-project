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

#To do fix tests
    def setUp(self):
        list_of_clubs = ClubList()
        self.club = list_of_clubs.create_new_club("Cambridge Chessinators", "Cambridge > Oxford", "Cambridge")
        for club in list_of_clubs.club_list:
            print(club.club_name)


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
        self.client.go
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'owner.html')

    # def test_redirect_when_not_owner(self):
    #     self.client.login(username=self.officer_user.username, password='Password123')
    #     response = self.client.get(self.url)
    #     response_url = reverse('profile')
    #     self.assertRedirects(response,response_url,status_code= 302, target_status_code= 200)
    #     self.assertTemplateUsed(response,'profile.html')


    def test_promote_member_to_officer(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self.member_user.groups.filter(name = self.club.getClubMemberGroup()).exists())
        self.assertFalse(self.member_user.groups.filter(name = self.club.getClubOfficerGroup()).exists())
        self.club.switch_user_role_in_club(self.member_user, "Officer")
        self.assertTrue(self.member_user.groups.filter(name = self.club.getClubOfficerGroup()).exists())
        self.assertFalse(self.member_user.groups.filter(name = self.club.getClubMemberGroup()).exists())
        # response = self.client.get(self.url)
        # response_url = reverse('owner_member_list')
        # self.assertRedirects(response,response_url,status_code= 302, target_status_code= 200)
        # self.assertTemplateUsed(response,'owner_member_list')

    def test_officer_can_be_demoted(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self.officer_user.groups.filter(name = self.club.getClubOfficerGroup()).exists())
        self.club.switch_user_role_in_club(self.officer_user, "Member")
        self.assertFalse(self.officer_user.groups.filter(name = self.club.getClubOfficerGroup()).exists())
        self.assertTrue(self.officer_user.groups.filter(name =self.club.getClubMemberGroup()).exists())
        # response = self.client.get(self.url)
        # response_url = reverse('officer_list')
        # self.assertRedirects(response,response_url,status_code= 302, target_status_code= 200)
        # self.assertTemplateUsed(response,'officer_list.html')


    def test_cannnot_promote_member_to_owner(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertFalse(self.member_user.groups.filter(name = self.club.getClubOfficerGroup()).exists())
        self.assertTrue(self.member_user.groups.filter(name = self.club.getClubMemberGroup()).exists())
        self.club.switch_user_role_in_club(self.member_user, "Owner")
        self.assertFalse(self.member_user.groups.filter(name= self.club.getClubOwnerGroup).exists())
        self.assertFalse(self.member_user.groups.filter(name = self.club.getClubOfficerGroup()).exists())
        # response = self.client.get(self.url)
        # response_url = reverse('owner_member_list')
        # self.assertRedirects(response,response_url,status_code= 302, target_status_code= 200)
        # self.assertTemplateUsed(response,'owner_member_list.html')


    def test_cannnot_promote_applicant_to_owner(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertFalse(self.applicant_user.groups.filter(name = self.club.getClubOfficerGroup()).exists())
        self.assertFalse(self.applicant_user.groups.filter(name = self.club.getClubMemberGroup()).exists())
        self.assertTrue(self.applicant_user.groups.filter(name=self.club.getClubApplicantGroup()).exists())
        self.club.switch_user_role_in_club(self.applicant_user, "Owner")
        self.assertFalse(self.applicant_user.groups.filter(name= self.club.getClubOwnerGroup).exists())
        self.assertFalse(self.applicant_user.groups.filter(name = self.club.getClubOfficerGroup()).exists())
        self.assertFalse(self.applicant_user.groups.filter(name = self.club.getClubMemberGroup()).exists())
        response = self.client.get(self.url)
        response_url = reverse('owner_member_list')
        self.assertRedirects(response,response_url,status_code= 302, target_status_code= 200)
        self.assertTemplateUsed(response,'owner_member_list.html')


    def test_officer_can_be_promoted(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self.officer_user.groups.filter(name = self.club.getClubOfficerGroup()).exists())
        self.owner.user_set.add(self.officer_user)
        self.assertTrue(self.user.groups.filter(name=self.club.getClubOwnerGroup()).exists())


    # def test_owner_change(self):
    #     response = self.client.post(self.url,self.other_user.id,follow=True)
    #     response_url = reverse('log_in')
    #     self.assertRedirects(response,response_url,status_code= 302, target_status_code= 200)
    #     self.assertTemplateUsed('log_in.html')
    #     owners = self.owner.user_set.getAll.toList
    #     current_owner = owners[0]
    #     self.owner.user_set.add(self.other_user)
    #     self.owner.user_set.remove(current_owner)
    #     owner_count = len((self.owner.user_set.all()).toList)
    #     self.assertEqual(owner_count,1)
    #     owners = self.owner.user_set.getAll.toList
    #     current_owner = owners[0]
    #     self.assertEqual(owners[0],self.other_user)
