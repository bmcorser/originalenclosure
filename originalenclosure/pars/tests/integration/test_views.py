from django.test import TestCase
from django_dynamic_fixture import G
from django.core.urlresolvers import reverse

from originalenclosure.tests.tools import log_me_in
from pars.models import Par, Image

class TestParsFunctions(TestCase):
    def setUp(self):
        images = [G(Image) for x in range(0,4)]
        G(Par, number='0001', title='first par',
            left=images[0], right=images[1])
        G(Par, number='0002', title='second par',
            left=images[2], right=images[3])

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
        data = {
            u'par-number': [u'0402'],
            u'par-title': [u'yeah yeah'],
            u'left-source': [u'http://originalenclosure.net/media/pars/AMCFsS51Zc32UqjDL._SL500_SS500_.jpg'],
            u'right-source': [u'https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Barrington_Hall_North.JPG/640px-Barrington_Hall_North.JPG'],
        }

        resp = self.client.post(reverse('make'),kwargs=data)
        self.assertEqual(resp.status_code, 200)
