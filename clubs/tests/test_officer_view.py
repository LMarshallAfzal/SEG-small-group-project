"""Test of the officer view"""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from clubs.forms import LogInForm
from clubs.models import User
from .helpers import LogInTester
from django.contrib.auth.models import Group

class OfficerViewTestCase(TestCase):
    """Tests of the officer view"""


    fixtures = [
        'clubs/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        self.url = reverse('officer')
        self.user = User.objects.get(username = 'johndoe@example.org')
        self.applicant = Group.objects.get(name = 'Applicant')
        self.member = Group.objects.get(name = 'Member')


    def test_officer_url(self):
        self.assertEqual(self.url, '/officer/')

    def test_applicant_can_be_accepted(self):

        self.member.user_set.add(self.user)
        self.applicant.user_set.remove(self.user)
        self.assertNotIn(self.user,self.applicant)
        self.asserIn(self.user,self.member)

    def test_applicant_can_be_rejected(self):
        before_count = User.objects.count()
        self.applicant.user_set.remove(self.user)
        User.objects.remove(self.user)
        self.assertNotIn(self.user,self.applicant)
        after_count = User.objects.count()
        self.assertEqual(after_count,before_count-1)


      
