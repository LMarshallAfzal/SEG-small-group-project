"""Test of the officer view"""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from clubs.forms import LogInForm
from clubs.models import User, Club
from clubs.club_list import ClubList
from clubs.tests.helpers import LogInTester
from django.contrib.auth.models import Group


class OfficerViewTestCase(TestCase):
    """Tests of the officer view"""

    fixtures = [
        'clubs/tests/fixtures/club.json',
        'clubs/tests/fixtures/member.json',
        'clubs/tests/fixtures/applicant.json',
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_user.json',
    ]

    def setUp(self):
        self.url = reverse('officer')
        self.user = User.objects.get(username='johndoe@example.org')
        self.other_user = User.objects.get(username = 'janedoe@example.org')
        # self.club = ClubList().find_club(club_name="The Buzzards")
        # self.applicant = Group.objects.get(name = self.club.getClubApplicantGroup())
        # self.applicant.user_set.add(user)

    def test_officer_url(self):
        self.assertEqual(self.url, '/officer/')

    def test_successful_applicant_acceptance(self):
        pass
        response = self.client.post(reverse('officer_promote_applicants'))
        #applicant_count = Group.objects.get(name = club.getClubApplicantGroup().count())
        self.assertEqual(response.status_code, 302)
        #self.assertEqual(applicant_count, 0)


    def test_successful_applicant_rejection(self):
        pass

    def test_officer_can_only_accept_applicants(self):
        pass

    def test_officer_can_only_reject_applicants(self):
        pass
