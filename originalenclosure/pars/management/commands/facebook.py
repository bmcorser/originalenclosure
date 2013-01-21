import requests
from datetime import date
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from pars.models import Par

class Command(BaseCommand):
  help = "Post to Facebook"

  def __init__(self,*args,**kwargs):
    pass

  def handle(self, *args, **kwargs):
    oauth_args = dict(client_id = settings.FACEBOOK_APP_ID,
        client_secret = settings.FACEBOOK_APP_SECRET,
        grant_type = 'client_credentials')
