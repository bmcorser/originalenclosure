from datetime import datetime
from django.db import models
from django.core.files import File

class Par(models.Model):
  class Meta:
    ordering = ['number','created']
  number = models.CharField(max_length=4,default='')
  title = models.CharField(max_length=200)
  hidden = models.BooleanField(default=False)
  created = models.DateTimeField(default=datetime.now())

  """ _     _____ _____ _____ 
     | |   | ____|  ___|_   _|
     | |   |  _| | |_    | |  
     | |___| |___|  _|   | |  
     |_____|_____|_|     |_|  """
   
  left_image = models.ImageField(
      max_length=10000,
      upload_to='pars',
      blank=True,
      )
  left_source = models.URLField(
      max_length=10000,
      )
  left_seen = models.DateField(
      default=datetime.now(),
      null=True,
      )
  left_dead = models.BooleanField(default=False)

  """ ____  ___ ____ _   _ _____ 
     |  _ \|_ _/ ___| | | |_   _|
     | |_) || | |  _| |_| | | |  
     |  _ < | | |_| |  _  | | |  
     |_| \_\___\____|_| |_| |_|  """

  right_image = models.ImageField(
      max_length=10000,
      upload_to='pars',
      blank=True,
      )
  right_source = models.URLField(
      max_length=10000,
      )
  right_seen = models.DateField(
      default=datetime.now(),
      null=True,
      )
  right_dead = models.BooleanField(default=False)


  def saved(self, *args, **kwargs):
    if all([self.left_source, self.right_source]) and not any([self.left_image, self.right_image]):
      self.left_image = File(self._image(self.left_source))
      self.right_image = File(self._image(self.right_source))
      super(Par, self).save()

  def _image(self,url):
    import requests, tempfile, os
    from urlparse import urlparse
    filename = urlparse(url).path.split('/')[-1]
    tmp = tempfile.NamedTemporaryFile(prefix="",suffix=filename)
    tmp.write(requests.get(url).content)
    return tmp

  def __unicode__(self):
    return ' '.join([self.number,self.title])
