# -*- coding: utf-8 -*-
import os, re
from time import sleep

import requests
from requests.auth import HTTPBasicAuth

from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from pars.models import Par, Image

from celery import task

from .purchases import make_pdf, make_png, make_gumroad_product

TIMEOUT = 30

@task
def sleep_task(n):
    sleep(n)
    return 'sleeping completed'

@task
def facebook():
    if settings.DEBUG:
        return
    if Par.objects.filter(in_buffer=True).count() > 17:

        def percent(model, filter):
            subject = float(model.objects.filter(**{filter: True}).count())
            context = float(model.objects.all().count())
            return subject/context*100

        description_dict = {
            'dead': '{:.2f}%'.format(percent(Image,'dead')),
            'redacted': '{:.2f}%'.format(percent(Par,'hidden'))
        }

        par_buffer = Par.objects.filter(in_buffer=True) 
        for par in par_buffer:
            if par.hidden:
                blank_words = [len(word)*'█' for word in par.title.split(' ')]
                par.title = ' '.join(blank_words)

        message_dict = {
            'pars': par_buffer
        }

        description = render_to_string('facebook/description.html',
                                       description_dict)
        message = render_to_string('facebook/message.html', message_dict)
        link = ''.join(['http://www.originalenclosure.net',reverse('parhome')])
        payload = {
            'name': 'Pars, 2010 © Ben Marshall-Corser.',
            'caption': 'New pars!',
            'description': description,
            'access_token': settings.FACEBOOK_ACCESS_TOKEN,
            'app_id': settings.FACEBOOK_APP_ID,
            'link': link,
            'message': message,
        }
        r = requests.post('https://graph.facebook.com/benmarshallcorser/feed/',
                          data=payload)
        print r.text
        if r.status_code == 200:
            Par.objects.filter(in_buffer=True).update(in_buffer=False)
    else:
        print 'nothing to do'
