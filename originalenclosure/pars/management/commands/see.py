import re, requests
from django.core.management.base import BaseCommand, CommandError
from pars.models import Par

class Command(BaseCommand):
  help = "Sees if par images are available at source"

  def __init__(self,*args,**kwargs):
    self.re = re.compile(r'^image')

  def handle(self, *args, **kwargs):
    for par in Par.objects.all():
      from ipdb import set_trace;set_trace()
      right_seen = self.see(par.right_source)
      left_seen = self.see(par.left_source)
      self.stdout.write('%s' % right_seen)

  def see(self,url):
    r = requests.head(url)
    return r.status_code == requests.codes.ok and self.re.match(r.headers['content-type'])
