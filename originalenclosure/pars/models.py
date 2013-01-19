from datetime import datetime
from django.db import models
from django.core.files import File

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

  def save(self, *args, **kwargs):
    if self.source and not self.image:
      self.image = File(self._image(self.source))
    super(Image, self).save()

  def _image(self,url):
    import requests, tempfile, os
    from urlparse import urlparse
    filename = urlparse(url).path.split('/')[-1]
    tmp = tempfile.NamedTemporaryFile(prefix="",suffix=filename)
    tmp.write(requests.get(url).content)
    return tmp

  def __unicode__(self):
    return ' '.join([self.image.name,'from',self.source])

class Par(models.Model):
  class Meta:
    ordering = ['number','created']
  number = models.CharField(max_length=4,default='')
  title = models.CharField(max_length=200)
  hidden = models.BooleanField(default=False)
  created = models.DateTimeField(default=datetime.now())
  left = models.OneToOneField(Image,related_name='left',null=True,blank=True)
  right = models.OneToOneField(Image,related_name='right',null=True,blank=True)

  def __unicode__(self):
    return ' '.join([self.number,self.title])

