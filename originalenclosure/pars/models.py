from datetime import datetime
from django.db import models

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
  slug = models.SlugField(max_length=1000000)

  def __unicode__(self):
    return ' '.join([self.number,self.title])

