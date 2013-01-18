import re, requests
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from pars.models import Par

class Command(BaseCommand):
  help = "Sees if par images are available at source"

  def __init__(self,*args,**kwargs):
    self.re = re.compile(r'^image')

  def handle(self, *args, **kwargs):
    for par in Par.objects.all():
      self.stdout.write('%s\n' % par.__repr__())
      for image in [image for image in [par.left,par.right] if image.source != '']:
        seen = self.seen(image.source)
        if seen:
          self.stdout.write('SEEN %s \n' % image.source)
        else:
          self.stdout.write('DID NOT SEE %s \n' % image.source)

  def seen(self,url):
    r = requests.head(url)
    return r.status_code == requests.codes.ok and self.re.match(r.headers['content-type']) != None
