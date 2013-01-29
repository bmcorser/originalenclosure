import re, tweepy
from datetime import date
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from pars.models import Par

class Command(BaseCommand):
  help = "Publish par to Twitter"

  def __init__(self,*args,**kwargs):
    pass

  def handle(self, *args, **kwargs):
    auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(settings.TWITTER_ACCESS_KEY, settings.TWITTER_ACCESS_SECRET)
    api = tweepy.API(auth)
    api.update_status('test')
