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
        ready = []
        ###################
        #### RUN START ####
        ###################
        run_start = datetime.now()

        # for par in Par.objects.all():
        for par in Par.objects.filter(created__gt=datetime.now() - timedelta(days=10)):
            temp_parsee = TempParSee(par,
                                     seen.delay(par.left),
                                     seen.delay(par.right))
            ready.append(temp_parsee)
        
        def _results(readies):
            readies_list = []
            for ready in readies:
                readies_list.extend([ready.l.ready(), ready.r.ready()])
            return readies_list

        while not all(_results(ready)):
            print '[{0}] waiting'.format(datetime.now())
            sleep(1)

        #################
        #### RUN END ####
        #################
        run_end = datetime.now()

        parseerun = ParSeeRun(start=run_start,
                              end=run_end)
        parseerun.save()

        for temp_parsee in ready:
            temp_parsee_result = u'{},{}'.format(int(temp_parsee.l.result),
                                     int(temp_parsee.r.result))
            ParSee(run=parseerun,
                   par=temp_parsee.par,
                   result=temp_parsee_result).save()
