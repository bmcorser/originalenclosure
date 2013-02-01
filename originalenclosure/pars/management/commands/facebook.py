import requests
from datetime import datetime
from datetime import date
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from pars.models import Par

class Command(BaseCommand):
  help = "Post to Facebook"

  def __init__(self,*args,**kwargs):
    pass

  def handle(self, *args, **kwargs):
    payload = {
        'access_token':settings.FACEBOOK_ACCESS_TOKEN,
        'message':str(datetime.now())+" a little message",
        'picture':'http://originalenclosure.net/media/pars/kUl37_3459862-864786-three-rolls-of-toilet-paper-isolated-on-the-white-background.jpg',
        'link':'http://www.originalenclosure.net/pars/411',
        'name':'0414 cast iron',
        }
    response = requests.post('https://graph.facebook.com/benmarshallcorser/feed',data=payload)
    print response
    # from ipdb import set_trace;set_trace()
