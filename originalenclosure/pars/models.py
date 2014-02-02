from datetime import datetime
import hashlib
import json
from os.path import join, isfile
import uuid
from subprocess import Popen

from bitfield import BitField
import requests
import tweepy
from xhtml2pdf import pisa

from django.db import models
from django.conf import settings
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse

from djmoney.models.fields import MoneyField

class Image(models.Model):
  image = models.ImageField(
      max_length=10000,
      upload_to='pars',
      blank=True,
      )
  source = models.URLField(
      max_length=10000,
      blank=True,
      null=True,
      )
  seen = models.DateField(
      default=datetime.now(),
      null=True,
      )
  dead = models.NullBooleanField(default=False,null=True,blank=True)

  def __unicode__(self):
    return ' '.join([self.image.name,'from',self.source])

class Par(models.Model):
    class Meta:
        ordering = ['number','created']
    number = models.CharField(max_length=4,default='')
    title = models.CharField(max_length=200)
    hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    left = models.OneToOneField(Image, related_name='left',
                                null=True, blank=True)
    right = models.OneToOneField(Image, related_name='right',
                                 null=True, blank=True)
    slug = models.SlugField(max_length=204, blank=True)
    in_buffer = models.BooleanField()

    def __unicode__(self):
        return ' '.join([self.number,self.title])

    def _run(self,offset=-1):
        trying = True
        count = 0
        position = offset
        while trying:
            try:
                return Par.objects.get(number='{0:04}'.format(int(self.number)
                                                              + position))
                trying = False
            except Par.DoesNotExist:
                count += 1
                position = count*offset
                pass
    
    def older(self,offset=-1):
        if offset > 0:
            if self == Par.objects.reverse()[:1][0]:
                return None
        else:
            if self == Par.objects.all()[0]:
                return None
        return self._run(offset=offset)

    @classmethod
    def latest(self):
        return Par.objects.filter(in_buffer=False).reverse()[:1][0]

    def tweet(self):
        """
        Send a tweet of this par to the account defined in settings.
        Will not happen if DEBUG = True
        """
        if settings.DEBUG:
            return
        auth = tweepy.OAuthHandler(
            settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
        auth.set_access_token(
            settings.TWITTER_ACCESS_KEY, settings.TWITTER_ACCESS_SECRET)
        api = tweepy.API(auth)
        template_dict = {
            'par':self,
            'date':self.created.strftime('%A %Y'),
            'url':reverse('permapar', kwargs={'slug':self.slug})
        }
        template = render_to_string('tweet.html',template_dict,)
        api.update_status(template)

class Purchase(models.Model):

    def make_uuid():
        return uuid.uuid4().get_hex()

    uuid = models.CharField(max_length=32,
                            primary_key=True,
                            default=make_uuid,
                            editable=False)
    par = models.ForeignKey(Par)
    sale = models.DateTimeField(auto_now_add=True)
    pdf = models.CharField(max_length=1000, null=True)
    gumroad_id = models.CharField(max_length=512,
                                  null=True,
                                  blank=True,
                                  default='')

    def _link_callback(self, uri, rel):
        s_u = settings.STATIC_URL
        s_r = settings.STATIC_ROOT
        m_u = settings.MEDIA_URL
        m_r = settings.MEDIA_ROOT

        if uri.startswith(m_u):
            path = join(m_r, uri.replace(m_u, ''))
        elif uri.startswith(s_u):
            path = join(s_r, uri.replace(s_u, ''))

        # make sure that file exists
        if not isfile(path):
                messge = 'media URI must start with %s or %s'.format(s_u, s_m)
                raise Exception(message)
        return path

    def make_pdf(self):
        from . import views
        html = views.par_pdf(self.par, self.uuid)
        pdf_path = join(settings.MEDIA_ROOT, 'pars', 'purchases', self.uuid)
        pdf = open(pdf_path, 'w+b')
        pisa_status = pisa.CreatePDF(html, dest=pdf,
                                     link_callback=self._link_callback)
        pdf.close()
        return pdf_path, pisa_status.err

    def make_png(self, pdf_path):
        purchases_path = join(settings.MEDIA_ROOT,
                              'pars',
                              'purchases')
        outpath = join(purchases_path, '{0}.png'.format(self.uuid))
        ghostscript_cmd = [
            'gs',
            '-sDEVICE=png16m',
            '-sOutputFile={0}'.format(outpath),
            '-r1200',
            '-dDownScaleFactor=6',
            '-dQUIET',
            '-dBATCH',
            '-dNOPAUSE',
            join(purchases_path, self.uuid),
        ]
        assert Popen(ghostscript_cmd).wait() == 0
        return outpath

    def make_gumroad_product(self):
        url = 'https://api.gumroad.com/v2/products'
        pdf_path, err = self.make_pdf()
        png_path = self.make_png(pdf_path)
        url_components = [
            settings.DOMAIN,
            settings.MEDIA_URL.strip('/'),
            'pars',
            'purchases',
        ]
        data = {
            'url': '/'.join(url_components + [self.uuid]),
            'preview_url': '/'.join(url_components + ['{0}.png'.format(self.uuid)]),
            'access_token': settings.GUMROAD_ACCESS_TOKEN,
            'name': '{0} ({1})'.format(self.par, self.uuid),
            'price': 100,
        }
        response = requests.post(url, data=data)
        response_dict = json.loads(response.content)
        self.gumroad_id = response_dict['product']['id']
        self.save()
        return response

class ParSeeRun(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()

class ParSee(models.Model):
    class Meta:
        get_latest_by = 'datetime'
    run = models.ForeignKey(ParSeeRun, related_name='parsees')
    par = models.ForeignKey(Par, related_name='parsees')
    result = BitField(flags=('left', 'right'), default=0)
    #result = models.CommaSeparatedIntegerField(max_length=3)
