from functools import wraps
from django.contrib.auth.models import User

def log_me_in(f):
    """
    Decorator to make the test method run as if user was logged in
       """
    def wrapper(self, *args, **kwargs):
        teardown_user = False
        if not hasattr(self, 'user'):
            self.password = 'jura'
            user = User.objects.create_superuser(
                username='test-dummy',
                email='test@dummy.com',
                password=self.password)
            teardown_user = True
            self.user = user

        self.client.login(username=self.user.username,
                          password=self.password)

        result = f(self, *args, **kwargs)

        #clean our mess to avoid side effect
        if teardown_user:
            user.delete()
            del self.user

        return result

    return wraps(f)(wrapper)
