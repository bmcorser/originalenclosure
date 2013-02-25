# -*- coding: utf-8 -*-

import requests
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from pars.models import Par, Image
from celery import task

@task
def facebook():
    if Par.objects.filter(in_buffer=True).count() > 34:

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
                par.title = ' '.join([len(word)*'█' for word in par.title.split(' ')])

        message_dict = {
            'pars': par_buffer
        }

        description = render_to_string('facebook/description.html', description_dict)
        message = render_to_string('facebook/message.html', message_dict)

        payload = {
            'name': 'Pars, 2010 © Ben Marshall-Corser.',
            'caption': 'New pars!',
            'description': description,
            'access_token': settings.FACEBOOK_ACCESS_TOKEN,
            'app_id': settings.FACEBOOK_APP_ID,
            'link': ''.join(['http://www.originalenclosure.net',reverse('parhome')]),
            'message': message,
        }
        r = requests.post('https://graph.facebook.com/benmarshallcorser/feed/',data=payload)
        print r.text
        if r.status_code == 200:
            Par.objects.filter(in_buffer=True).update(in_buffer=False)
    else:
        print 'nothing to do'
