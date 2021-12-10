from django.test import TestCase
from django.urls import reverse
from clubs.models import User
from clubs.tests.helpers import reverse_with_next

class ShowUserTest(TestCase):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_user.json'
    ]

    def setUp(self):
        self.user = User.objects.get(email='johndoe@example.org')
        self.target_user = User.objects.get(email='janedoe@example.org')
        self.url = reverse('show_user', kwargs={'user_id': self.target_user.id})

    def test_show_user_url(self):
        self.assertEqual(self.url,f'/user/{self.target_user.id}')

    def test_get_show_user_with_valid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_user.html')
        self.assertContains(response, "Jane Doe")

    def test_get_show_user_with_own_id(self):
        self.client.login(email=self.user.username, password='Password123')
        url = reverse('show_user', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_user.html')
        self.assertContains(response, "John Doe")

    # def test_show_user_with_invalid_id(self):
    #     self.client.login(username=self.user.username, passsword='Password123')
    #     url = reverse('show_user', kwargs={'user_id': self.user.id+999})
    #     response = self.client.get(url,follow=True)
    #     response_url = reverse('member_list')
    #     self.assertRedirects(response, response_url,status_code=302,target_status_code=200)
    #     self.assertTemplateUsed(response,'member_list.html')