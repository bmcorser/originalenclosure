from django.core.files import File
from django.db.models.signals import pre_save
from django.dispatch import receiver
from models import Image

def _image(url):
  import requests, tempfile, os
  from urlparse import urlparse
  filename = urlparse(url).path.split('/')[-1]
  tmp = tempfile.NamedTemporaryFile(prefix="",suffix=filename)
  tmp.write(requests.get(url).content)
  return tmp

@receiver(pre_save,sender=Image, dispatch_uid="par.image.download")
def download(sender,instance,**kwargs):
  if instance.source and not instance.image:
    instance.image = File(_image(instance.source))
  elif Image.objects.get(pk=instance.pk).source != instance.source:
    instance.image.delete()
    tmp = _image(instance.source)
    instance.image = File(tmp)
    del(tmp)


