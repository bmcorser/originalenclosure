# -*- coding: utf-8 -*-
import os, re

import requests
from requests.auth import HTTPBasicAuth

from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from pars.models import Par, Image

from celery import task


TIMEOUT = 30


@task
def facebook():
    if settings.DEBUG:
        return
    if Par.objects.filter(in_buffer=True).count() > 17:

        def percent(model, filter):
            kwargs = {filter: True}
            subject = float(model.objects.filter(**kwargs).count())
            context = float(model.objects.all().count())
            return subject/context*100

        description_dict = {
            'dead': '{:.2}%'.format(percent(Image,'dead')),
            'redacted': '{:.2}%'.format(percent(Par,'hidden'))
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

@task
def make_gumroad_product(par):
    webhook_string = 'http://www.originalenclosure.net/pars/gumroad/{0}'
    webhook_url = webhook_string.format(par.hash())
    description_string = 'Ownership of par number {0}, entitled {1}'
    description = description_string.format(par.number, par.title)
    payload = {'name': par.__unicode__(),
               'url': 'http://www.originalenclosure.net/static/pars/par.pdf',
               'price': 100,
               'description': description,
               'country_available': 'UK',
               'max_purchase_count': 1,
               'customizable_price': 'true',
               'webhook': webhook_url,
               'require_shipping':'false',
               'shown_on_profile':'false'}
    files = {'preview': open(os.path.join(settings.MEDIA_ROOT,'par.jpg'))}
    response =  requests.post(
        settings.GUMROAD_API_URL,
        data=payload,
        files=files,
        auth=HTTPBasicAuth(settings.GUMROAD_TOKEN, '',))
    return response.status_code, response.content


@task
def seen(image):
    try:
        url = image.source
    except AttributeError:
        return False
    # here we go with returning an asyncresult object to poll on
    if url == '':
        return False
    ua = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT; python requests)'
    try:
        r = requests.head(url, headers={'User-Agent': ua}, timeout=TIMEOUT)
    except (requests.exceptions.ConnectionError,
            requests.exceptions.Timeout):
        r = requests.Response()
    regex = re.compile(r'^image')
    if not r.status_code == requests.codes.ok:
        return False
    if not r.headers['content-type']:
        r = requests.get(url, headers=headers, timeout=TIMEOUT)
        if not r.headers['content-type']:
            return False
    return bool(regex.match(r.headers['content-type']))
