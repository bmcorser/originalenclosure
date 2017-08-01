# -*- coding: utf-8 -*-
from collections import namedtuple
from datetime import datetime, timedelta
import re
import urllib
import time

from django.core.management.base import BaseCommand
from django.db.models import Q
from time import sleep
import grequests
import requests
import djcelery
from pars.models import ParSeeRun, ParSee, Image, Par

TIMEOUT = 5
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36'}
IMAGE_REGEX = re.compile(r'^[iI]mage')
PROXY_URL = 'http://www.proxy-service.de/proxy-service.php?u='
FAIL_TEMPLATE = '''
===
ID:     {0}
RESP:   {1}
TYPE:   {2}
SOURCE: {3}
'''

class ImageHasNoSource(Exception):
    pass

def get_url(image):
    try:
        url = image.source
        if not url:
            raise ImageHasNoSource(image)
        return url
    except AttributeError:
        raise ImageHasNoSource(image)
        

def seen(url, method):
    fn = getattr(requests, method)
    print('===')
    print(url)
    tries = 0
    while tries < 2:
        try:
            tries += 1
            resp = fn(
                # PROXY_URL + urllib.quote(url, ''),
                url,
                headers=HEADERS,
                timeout=TIMEOUT
            )
            print(resp)
            print(resp.headers.get('content-type'))
            return resp
        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionsError,
        ) as exc:
            time.sleep(0.5)
            pass

def exception_handler(req, exc):
    print(exc.__class__.__name__)
    return False

def append_dead_return_failed(responses, images, dead):
    failed = []
    for index, resp in enumerate(responses):
        if isinstance(resp, Exception) or not resp:
            resp_failed = True
        else:
            resp_failed = any((
                resp.status_code != requests.codes.ok,
                not resp.headers['content-type'],
            ))
        if resp_failed:
            if resp is not None:
                print(FAIL_TEMPLATE.format(
                    images[index].id,
                    resp,
                    resp.headers.get('content-type'),
                    images[index].source)
                )
            else:
                print("SERVER DEAD: {0}".format(images[index]))
            failed.append(images[index])
            continue
        if not IMAGE_REGEX.match(resp.headers['content-type']):
            dead.append(images[index])
        not_dead = all((
            resp.status_code == requests.codes.ok,
            IMAGE_REGEX.match(resp.headers['content-type']),
        ))
        if not_dead:
            images[index].dead = False
            images[index].save()
    return failed

class Command(BaseCommand):
    help = "Sees if par images are available at source"

    def handle(self, *args, **kwargs):
        """
        Command to make a ParSeeRun and record all the ParSees
        """
        TempParSee = namedtuple('TempParSee', ['par','l','r'])
        results = []
        ###################
        #### RUN START ####
        ###################
        run_start = datetime.now()

        dead = []

        heads_images = []
        heads = []
        # images = Image.objects.all();
        images = Image.objects.filter(Q(dead=True), Q(right__isnull=False) | Q(left__isnull=False));
        # pars = Par.objects.all()
        # pars = Par.objects.filter(
            # created__gt=datetime.now() - timedelta(days=60))
        # par = Par.objects.filter(number='1099')[0]
        for image in images:
        # for image in [par.right]:
            try:
                # heads.append(seen(get_url(image), 'head'))
                # heads_images.append(image)
                dead.extend(append_dead_return_failed([seen(get_url(image), 'head')], [image], dead))
            except ImageHasNoSource as exc:
                print(exc)

        # gets_images = append_dead_return_failed(heads, heads_images, dead)
        # gets = [seen(image.source, 'get') for image in gets_images]
        # dead.extend(append_dead_return_failed(gets, gets_images, dead))
        '''
        for image in dead:
            print(getattr(image, 'source'))
            image.dead = True
            image.save()
        
        #################
        #### RUN END ####
        #################
        run_end = datetime.now()

        parseerun = ParSeeRun(start=run_start,
                              end=run_end)
        parseerun.save()

        def _temp_to_db(temp_parsee):
            parsee = ParSee(run=parseerun,
                            par=temp_parsee.par)
            parsee.result.left=temp_parsee.l.result
            parsee.result.right=temp_parsee.r.result
            parsee.save()
            self.stdout.write('Finished looking at {0}\n'.format(parsee.par))

        map(_temp_to_db, so_far)
        '''
