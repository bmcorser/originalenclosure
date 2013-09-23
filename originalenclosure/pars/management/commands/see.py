# -*- coding: utf-8 -*-
from collections import namedtuple
from datetime import datetime
from django.core.management.base import BaseCommand
from time import sleep
import djcelery
from pars.models import Par
from pars.tasks import seen

class Command(BaseCommand):
    help = "Sees if par images are available at source"

    def handle(self, *args, **kwargs):
        ParSee = namedtuple('ParSee', ['par','l','r'])
        results = []
        for par in Par.objects.all():
            parsee = ParSee(par,
                            seen.delay(par.left),
                            seen.delay(par.right))
            results.append(parsee)
        
        def _ready(results):
            result_list = []
            for result in results:
                result_list.extend([result.l.ready(), result.r.ready()])
            return result_list

        while not all(_ready(results)):
            print '[{0}] waiting'.format(datetime.now())
            sleep(1)

        def _len(parsee):
            return len(unicode(parsee.par))

        width = max([_len(parsee) for parsee in results])
        for parsee in results:
            graphics = {True: u'☆', False: u'☠'}
            gap = width - _len(parsee)
            print u'{0} {1} [{2}{3}]'.format(parsee.par, u'‧' * gap,
                                            graphics[parsee.l.result],
                                            graphics[parsee.r.result])
