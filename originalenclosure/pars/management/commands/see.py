# -*- coding: utf-8 -*-
from collections import namedtuple
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.conf import settings
from pars.models import Par
from pars.tasks import seen

class Command(BaseCommand):
    help = "Sees if par images are available at source"

    def handle(self, *args, **kwargs):
        print '{0} apparently'.format(settings.CELERY_RESULT_BACKEND)
        results = []
        ParSee = namedtuple('ParSee', ['par', 'left_seen', 'right_seen'])
        for par in Par.objects.filter(created__gt=datetime.now() - timedelta(days=10)):
            parsee = ParSee(par, seen.delay(par.left), seen.delay(par.right))
            results.append(parsee)
            print 'Added job for {0}'.format(par)

        for l_async, r_async in [(result.left_seen, result.right_seen) for result in results]:
            print l_async.state
            print r_async.state
