'''
zatim bez uspechu,
pytest nasel testy az po prejmenovani tests->test_accounts
a pada nejakou spolecnou zahadnou chybou
manage.py test pada 2 individualnimi chybami

from django.conf import settings
from django.urls import resolve, reverse
from django.test import TestCase
from .views import signup


class TestSignUp(TestCase):
    def test_signup_status_code(self):
        import pdb; pdb.set_trace()
        urls_public = getattr(settings, 'PUBLIC_SCHEMA_URLCONF', None)  # django-tenant-schemas
        if urls_public is None:
            url = reverse('accounts:signup')
        else:
            url = reverse('accounts:signup', urlconf=settings.PUBLIC_SCHEMA_URLCONF)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        import pdb; pdb.set_trace()
        view = resolve('/accounts/signup/')
        self.assertEquals(view.func, signup)
'''
