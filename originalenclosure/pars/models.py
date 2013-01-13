from django.db import models

class Par(models.Model):
  title = models.CharField(max_length=200)

  left_image = models.ImageField(upload_to='pars')
  left_url = models.URLField(max_length=10000)
  left_seen = models.DateField()
  left_dead = models.BooleanField()

  right_image = models.ImageField(upload_to='pars')
  right_url = models.URLField(max_length=10000)
  right_seen = models.DateField()
  right_dead = models.BooleanField()

  hidden = models.BooleanField()

  def save(self, *args, **kwargs):
    if self.left_url and self.right_url:
      self.left_image = self._image(self.left_url)
      self.right_image = self._image(self.right_url)
      super(Par, self).save()

  def _image(url):
    import requests, tempfile, os
    from urlparse import urlparse
    filename = urlparse(url).path.split('/')[-1]
    tmp = tempfile.TemporaryFile()
    tmp.write(requests.get(url).content())
    return tmp
