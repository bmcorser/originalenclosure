import tempfile, os
import requests
from urlparse import urlparse
from slugify import slugify
from django.conf import settings
from django.core.files import File
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from models import Par, Image, Purchase

def _image(url):
    filename = urlparse(url).path.split('/')[-1]
    tmp = tempfile.NamedTemporaryFile(prefix="",suffix=filename)
    tmp.write(requests.get(url).content)
    return tmp

@receiver(pre_save, sender=Image, dispatch_uid="par.image.download")
def download(sender, instance, **kwargs):
    if instance.source and not instance.image:
        # this hasn't been run before
        instance.image = File(_image(instance.source))
    else:
        try:
            existing_image = Image.objects.get(pk=instance.pk)
            if existing_image.source != instance.source:
                instance.image.delete(save=False)
                tmp = _image(instance.source)
                instance.image = File(tmp)
                del(tmp)
        except Image.DoesNotExist:
            # we are just importing
            pass

@receiver(pre_delete, sender=Purchase, dispatch_uid="par.purchase.delete")
def clean_purchase(sender, instance, **kwargs):
    purchases_path = os.path.join(settings.MEDIA_ROOT, 'pars', 'purchases')
    os.remove(os.path.join(purchases_path, instance.pdf))
    os.remove(os.path.join(purchases_path, '{0}.png'.format(instance.uuid)))

@receiver(pre_save,sender=Par, dispatch_uid="par.slug.maker")
def make_slug(sender,instance,**kwargs):
    instance.slug = slugify(' '.join([instance.number,instance.title]))
