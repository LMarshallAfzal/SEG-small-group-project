class LogInTester:
    def _is_logged_in(self):
        return 'auth_user_id' in self.client.session.keys()
