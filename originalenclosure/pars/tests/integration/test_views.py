from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

from originalenclosure.tests.tools import log_me_in
from pars.models import Par, Image

from pars.tests import factories

class TestParsFunctions(TestCase):
    def setUp(self):
        for _ in range(0,10):
            factories.ParFactory()

    @log_me_in
    def test_get_swap_200(self):
        """
        The view at the end of the URL pattern called 'swap' view returns a 200.
        """
        par = Par.objects.all()[0]
        resp = self.client.get(
            reverse('swap', kwargs={'par': par.number}), follow=True)
        self.assertEqual(resp.status_code, 200)

    @log_me_in
    def test_get_make_200(self):
        """
        The view at the end of the URL pattern called 'make' returns a 200
        """
        resp = self.client.get(reverse('make'), follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_get_pars_200(self):
        """
        Throw some numbers at the view behind the 'par' URL pattern and get some 200s back.
        """
        resp = self.client.get(reverse('par',args=('0010',)))
        self.assertEqual(resp.status_code, 200)

    @log_me_in
    @override_settings(DEBUG=True)
    def test_post_make_200(self):
        """
        POSTing data to the view behind 'make' returns a 200 and creates a par
        """
        data = {
            "par-number": ["0500"],
            "par-title": ["unexpectorant detractor"],
            "left-source": ["https://www.google.co.uk/images/srpr/logo4w.png"],
            "right-source": ["https://www.google.co.uk/images/srpr/logo4w.png"]
        }

        resp = self.client.post(reverse('make'), data=data, follow=True)
        self.assertEqual(resp.status_code, 200)
