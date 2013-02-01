from datetime import datetime
import tweepy
from django.db import models
from django.conf import settings
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse

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
    left = models.OneToOneField(Image,related_name='left',null=True,blank=True)
    right = models.OneToOneField(Image,related_name='right',null=True,blank=True)
    slug = models.SlugField(max_length=1000000,blank=True)
    in_buffer = models.BooleanField()
  
    def __unicode__(self):
        return ' '.join([self.number,self.title])

    def _run(self,offset=-1):
        trying = True
        count = 0
        position = offset
        while trying:
            try:
                return Par.objects.get(number='{0:04}'.format(int(self.number)+position))
                trying = None
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
    def latest(self,par):
        if not par:
            return self.objects.all().reverse()[:1][0]
        else:
            return self.objects.get(number=par)

    def tweet(self):
        auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
        auth.set_access_token(settings.TWITTER_ACCESS_KEY, settings.TWITTER_ACCESS_SECRET)
        api = tweepy.API(auth)
        template_dict = {
            'par':self,
            'date':self.created.strftime('%A %Y'),
            'url':reverse('permapar', args=[self.slug])
        }
        template = render_to_string('tweet.html',template_dict,)
        api.update_status(template)
