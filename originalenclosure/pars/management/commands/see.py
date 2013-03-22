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
        text = urwid.Text('yeah')
        fill = urwid.Filler(text, 'middle')
        pars = []
        def grab_pars(loop, *args):
            for par in Par.objects.all()[:20]:
                parsee = ParSee()
                parsee.left_seen = seen.delay(par.left)
                parsee.right_seen = seen.delay(par.right)
                pars.append(parsee)
            loop.set_alarm_in(1, change_text)
        loop = urwid.MainLoop(urwid.Filler(urwid.Text(unicode([str(par) for par in pars])), 'middle'))
        def change_text(loop, *args, **kwargs):
            loop.widget = urwid.Filler(urwid.Text([unicode(par) for par in pars]), 'middle')
            loop.set_alarm_in(1, change_text)
        grab_pars(loop)
        loop.run()
