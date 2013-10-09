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

        # for par in Par.objects.all():
        for par in Par.objects.filter(created__gt=datetime.now() - timedelta(days=20)):
            temp_parsee = TempParSee(par,
                                     seen.delay(par.left),
                                     seen.delay(par.right))
            results.append(temp_parsee)
        
        def _ready(result):
            return all([result.l.ready(), result.r.ready()])

        so_far = []
        while not all(map(_ready, results)):
            print '[{0}] waiting'.format(datetime.now())
            this_poll = [result.par for result in results
                         if result.par not in so_far
                         and _ready(result)]
            so_far.append(this_poll)
            for par in this_poll:
                self.stdout.write(par)
            sleep(.1)

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

        map(_temp_to_db, ready)
