from django.test import TestCase
from clubs.models import User
from django.urls import reverse

class HomeViewTestCase(TestCase):
    """Tests for home view"""

    fixtures = ['clubs/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('home')
        self.user = User.objects.get(username = 'johndoe@example.org')

    def test_home_url(self):
        self.assertEqual(self.url,'/')

    def test_get_home(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
<<<<<<< HEAD

    def test_get_home_redirects_when_logged_in(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('club_selection')
        self.assertRedirects(response, redirect_url, status_code=302,target_status_code=200)
        self.assertTemplateUsed(response, 'club_selection.html')
=======
>>>>>>> f02286fb06efeb4dca2b68612a253146cc5ee414
