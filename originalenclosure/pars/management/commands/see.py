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
        ParSee = namedtuple('ParSee', ['par', 'l', 'r'])
        for par in Par.objects.filter(created__gt=datetime.now() - timedelta(days=10)):
            parsee = ParSee(par, seen.delay(par.left), seen.delay(par.right))
            results.append(parsee)
            print 'Added job for {0}'.format(par)

        for result in results:
            print result.l.result, result.r.result
