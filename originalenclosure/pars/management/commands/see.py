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
      if par.left_source != '' and par.right_source != '':
        self.stdout.write('%s' % par.__repr__())
        if self.seen(par.left_source):
          par.left_seen = datetime.now()
        else:
          par.left_dead = True
        if self.seen(par.right_source):
          par.right_seen = datetime.now()
        else:
          par.right_dead = True
        par.save()
        self.stdout.write('%s' % par.__dict__)

  def seen(self,url):
    r = requests.head(url)
    return r.status_code == requests.codes.ok and self.re.match(r.headers['content-type']) != None
