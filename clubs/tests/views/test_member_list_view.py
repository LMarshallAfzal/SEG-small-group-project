from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from clubs.models import User
from clubs.tests.helpers import reverse_with_next

class TestMemberListView(TestCase):
    """Tests for the member list view"""

    fixtures = [
        'clubs/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        self.url = reverse('member_list')
        self.user = User.objects.get(username='johndoe@example.org')

    def test_user_list_url(self):
        self.assertEqual(self.url, '/member_list/')

    def test_get_member_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302,target_status_code=200)
