# -*- coding: utf-8 -*-
import re, requests, urlparse, urwid
from datetime import date
from django.core.management.base import BaseCommand, CommandError
import djcelery
from pars.models import Par
from pars.tasks import seen
import time
from celery import Celery

class ParSee(object):

    seen = None

    def __unicode__(self):
        l = self.left_seen.wait()
        r = self.right_seen.wait()
        def f(r):
            if r == False:
                return u'☺'
            return '.'
        return f(l)+u''+f(r)+''

class Command(BaseCommand):
    help = "Sees if par images are available at source"

    def handle(self, *args, **kwargs):
        for par in Par.objects.all():
            parsee = ParSee()
            parsee.left_seen = seen.delay(par.left)
            parsee.right_seen = seen.delay(par.right)
            print parsee.__unicode__()
