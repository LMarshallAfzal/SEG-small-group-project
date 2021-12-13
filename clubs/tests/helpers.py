<<<<<<< HEAD
from django.urls import reverse


def reverse_with_next(url_name,next_url):
      url=reverse(url_name)
      url += f"?next={next_url}"
      return url

class LogInTester:
    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()

=======
class LogInTester:
    def _is_logged_in(self):
        return 'auth_user_id' in self.client.session.keys()
>>>>>>> 63505a1f4aee82cc90ff1d9f2e729f3dbe71f45f
