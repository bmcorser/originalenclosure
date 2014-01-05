import hashlib
from datetime import datetime
from os.path import join, isfile
import uuid

import tweepy
from bitfield import BitField
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
        html = views.par(None,
                         self.par.number,
                         template_name='par_pdf.html').content
        pdf_path = join(settings.MEDIA_ROOT, 'pars', 'purchases', self.uuid)
        pdf = open(pdf_path, 'w+b')
        pisa_status = pisa.CreatePDF(html, dest=pdf,
                                     link_callback=self._link_callback)
        pdf.close()
        return pdf_path, pisa_status.err

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
