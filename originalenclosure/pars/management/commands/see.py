# -*- coding: utf-8 -*-
from collections import namedtuple
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from time import sleep
import djcelery
from pars.models import ParSeeRun, ParSee, Par
from pars.tasks import seen

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

        for par in Par.objects.filter(created__gt=datetime.now() - timedelta(days=10)):
            temp_parsee = TempParSee(par,
                                     seen.delay(par.left),
                                     seen.delay(par.right))
            results.append(temp_parsee)
        
        def _ready(results):
            result_list = []
            for result in results:
                finished = all([result.l.ready(), result.r.ready()])
                result_list.append(finished)
            return result_list

        while not all(_ready(results)):
            print '[{0}] waiting'.format(datetime.now())
            sleep(1)

        #################
        #### RUN END ####
        #################
        run_end = datetime.now()

        parseerun = ParSeeRun(start=run_start,
                              end=run_end)
        parseerun.save()

        for temp_parsee in results:
            from ipdb import set_trace;set_trace()
            temp_parsee_result = u'{},{}'.format(int(temp_parsee.l.result),
                                     int(temp_parsee.r.result))
            ParSee(run=parseerun,
                   par=temp_parsee.par,
                   result=temp_parsee_result).save()
