from datetime import datetime
import hashlib
import json
from os.path import join, isfile
from os import remove
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
    build = models.DateTimeField(auto_now_add=True)
    sale = models.DateTimeField(null=True)
    pdf = models.CharField(max_length=1000, null=True)
    gumroad_id = models.CharField(max_length=512,
                                  null=True,
                                  blank=True,
                                  default='')

    def __unicode__(self):
        return '{0} ({1})'.format(self.par, self.uuid)

    def build_url(self, ext):
        assert self.uuid
        assert self.par
        url_components = (
            settings.DOMAIN,
            settings.MEDIA_URL.strip('/'),
            'pars',
            'purchases',
            '{0}-{1}.{2}'.format(self.par.slug, self.uuid, ext),
        )
        return '/'.join(url_components)

    def build_path(self, ext):
        assert self.uuid
        assert self.par
        path_components = (
            settings.MEDIA_ROOT,
            'pars',
            'purchases',
            '{0}-{1}.{2}'.format(self.par.slug, self.uuid, ext),
        )
        return join(*path_components)

    @property
    def png_url(self):
        return self.build_url('png')

    @property
    def pdf_url(self):
        return self.build_url('pdf')

    @property
    def png_path(self):
        return self.build_path('png')

    @property
    def pdf_path(self):
        return self.build_path('pdf')

    def serialise(self, extra={}):
        return_dict = {
            'uuid': self.uuid,
            'pdf_url': self.pdf_url,
            'png_url': self.png_url,
            'gumroad_id': self.gumroad_id,
        }
        return_dict.update(extra)
        return return_dict


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
