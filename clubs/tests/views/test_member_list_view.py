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

    # def _create_test_users(self, user_count):
    #     for user_id in range(user_count):
    #         User.objects.get(f'user{user_id}@example.org',
    #         email=f'user{user_id}@example.org',
    #         password='Password123',
    #         first_name=f'First{user_id}',
    #         last_name=f'Last{user_id}',
    #         bio=f'Bio{user_id}',
    #         experience_level=f'Experience{user_id}',
    #         personal_statment=f'Statement{user_id}',
    #         )
