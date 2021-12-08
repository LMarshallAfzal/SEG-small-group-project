from django.test import TestCase
from django.urls import reverse
from clubs.models import User
# from clubs.tests.helpers import reverse_with_next

class TestMemberListView(TestCase):

    fixtures = [
        'clubs/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        self.url = reverse('member_list')
        self.user = User.objects.get(username='johndoe@example.org')

    def test_user_list_url(self):
        self.assertEqual(self.url, '/member_list/')
