import re, requests, urlparse
from datetime import date
from django.core.management.base import BaseCommand, CommandError
from pars.models import Par

class Command(BaseCommand):
  help = "Sees if par images are available at source"

  def __init__(self,*args,**kwargs):
    self.re = re.compile(r'^image')

  def handle(self, *args, **kwargs):
    for par in Par.objects.all():
      self.stdout.write('%s\n' % par.__repr__())
      for image in [i for i in [par.left,par.right] if i.source != '']:
        seen = self.seen(image.source)
        if seen:
          image.seen = date.today()
          image.dead = False
          image.save()
          self.stdout.write('SEEN %s\n' % image.source)
        else:
          image.dead = True
          image.save()
          self.stdout.write('DID NOT SEE %s\n' % image.source)

  def seen(self,url):
    try:
      r = requests.head(url)
    except requests.exceptions.ConnectionError:
      self.stdout.write('server error from %s\n' % urlparse.urlparse(url).netloc)
      r = requests.Response()
    return r.status_code == requests.codes.ok and self.re.match(r.headers['content-type']) != None
