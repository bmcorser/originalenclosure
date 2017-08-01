# -*- coding: utf-8 -*-
import os, re
from time import sleep

from celery import task
import facebook as fb_api
import requests
from requests.auth import HTTPBasicAuth

from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from pars.models import Par, Image
from .purchases import make_pdf, make_png, make_gumroad_product

TIMEOUT = 30

@task
def sleep_task(n):
    sleep(n)
    return 'sleeping completed'

def encoded_dict(in_dict):
    out_dict = {}
    for k, v in in_dict.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf8')
        elif isinstance(v, str):
            # Must be encoded in UTF-8
            v.decode('utf8')
        out_dict[k] = v
    return out_dict

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
        picture = None
        for par in par_buffer:
            if par.hidden:
                blank_words = [len(word)*'█' for word in par.title.split(' ')]
                par.title = ' '.join(blank_words)
            picture = 'http://originalenclosure.net' + par.left.image.url

        message_dict = {
            'pars': par_buffer
        }

        description = render_to_string('facebook/description.html',
                                       description_dict)
        message = render_to_string('facebook/message.html', message_dict)
        link = ''.join(['http://originalenclosure.net',reverse('parhome')])
        payload = {
            'name': 'Pars, 2010 © Ben Marshall-Corser.',
            'link': link,
            'caption': 'New pars!',
            'description': description,
            'picture': picture,
        }
        graph = fb_api.GraphAPI(settings.FACEBOOK_ACCESS_TOKEN)
        resp = graph.put_wall_post(
            message=message.encode('utf8'),
            attachment=encoded_dict(payload)
        )
        print resp
        if 'id' in resp:  # assume everything's ok
            Par.objects.filter(in_buffer=True).update(in_buffer=False)
    else:
        print 'nothing to do'
