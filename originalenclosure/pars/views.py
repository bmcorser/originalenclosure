#coding: utf-8
from datetime import datetime
import json
from os.path import join

from celery import chain

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from .models import ParSeeRun, ParSee, Par, Purchase
from . import purchases
from .forms import ParForm, ImageForm
from .tasks import (
    sleep_task,
    make_pdf,
    make_png,
    make_gumroad_product,
)

def legacy_par(request,par):
    try:
        par = Par.get(number='{0:04}'.format(int(par)))
    except Par.DoesNotExist:
        return HttpResponseRedirect(reverse('par'))
    return HttpResponseRedirect(
        reverse('par', kwargs={'par':par.number}))

def par(request, par=None, template_name='par.html'):
    if par:
        try:
            par = Par.objects.get(number=par)
        except Par.DoesNotExist:
            return HttpResponseRedirect(
                reverse('par', args=['{0:04}'.format(int(par))]))
    else:
        par = Par.latest()
    older = par.older()
    template_dict = {
            'older':older,
            'par':par,
            'date':par.created.strftime('%A %Y'),
        }
    if par.hidden:
        template_dict['title_split'] = par.title.split(' ')
    return render_to_response(template_name, template_dict)

def par_pdf(par, uuid):
    template_dict = {'uuid': uuid, 'par': par,
                     'date':par.created.strftime('%A %Y')}
    return render_to_string('par_pdf.html', template_dict)

def permapar(request,slug):
  par = Par.objects.get(slug=slug)
  template_dict = {
          'older':par.older(),
          'par':par,
          'date':par.created.strftime('%A %Y'),
      }
  if par.hidden:
      template_dict['title_split'] = par.title.split(' ')
  return render_to_response(
      'par.html',
      template_dict
  )

@login_required
def edit(request,par):
    try:
        par = Par.objects.get(number=par)
    except Par.DoesNotExist:
        return HttpResponseRedirect(reverse('par', args=['{0:04}'.format(int(par))]))
    if request.method == 'POST':
        par_form = ParForm(request.POST,instance=par,prefix="par").save()
        left = ImageForm(request.POST,instance=par.left,prefix="left").save()
        right = ImageForm(request.POST,instance=par.right,prefix="right").save()
    par_form = ParForm(prefix="par",instance=par)
    left_form = ImageForm(prefix="left",instance=par.left)
    right_form = ImageForm(prefix="right",instance=par.right)
    return render_to_response("edit.html", {
        "older":par.older(),
        "newer":par.older(1),
        "par":par,
        "par_form":par_form,
        "left_form":left_form,
        "right_form":right_form,
    },
    context_instance=RequestContext(request))

@login_required
def swap(request,par):
    par = Par.objects.get(number=par)
    par.left, par.right = par.right, par.left
    par.save()
    return HttpResponseRedirect(reverse('edit', args=[par.number]))

@login_required
def make(request):
  last = Par.objects.all()[len(Par.objects.all())-1]
  next = '{0:04}'.format(int(last.number)+1)
  if request.method == 'POST':
    par = ParForm(request.POST,prefix="par")
    left = ImageForm(request.POST,prefix="left")
    right = ImageForm(request.POST,prefix="right")
    par = par.save()
    par.left = left.save()
    par.right = right.save()
    par.save()
    par.tweet()
    return HttpResponseRedirect(reverse('make'))
  else:
    numbered_par = Par(number=next, in_buffer=True)
    par = ParForm(prefix="par",instance=numbered_par)
    left = ImageForm(prefix="left",instance=None)
    right = ImageForm(prefix="right",instance=None)
    last = Par.objects.all()[len(Par.objects.all())-1]
    return render_to_response("make.html", {
      "last":last,
      "par":par,
      "left":left,
      "right":right,
    },
    context_instance=RequestContext(request))

class ParSeeRunsView(ListView):
    queryset = ParSeeRun.objects.prefetch_related().all()
    template_name = 'pars/parseeruns.html'
    context_object_name = 'parseeruns'

def purchase(request, slug):
    par = Par.objects.get(slug=slug)
    purchase = Purchase(par=par)
    purchase.save()
    task_chain = chain(make_pdf.s(purchase),
                       make_png.s(),
                       make_gumroad_product.s())()

    def add_parents(task, list_=[]):
        list_.insert(0, {
            'id': task.id,
            'name': task.task_name,
        })
        if not task.parent:
            return list_
        return add_parents(task.parent, list_)

    task_list = add_parents(task_chain)

    template_dict = {
        'purchase': purchase.serialise(),
        'task_list': json.dumps(task_list),
    }
    return render_to_response('pars/purchase.html', template_dict)


@csrf_exempt
def gumroad_ping(request):
    purchase = Purchase.objects.get(gumroad_id=request.POST['permalink'])
    purchase.sale = datetime.now()
    purchase.save()
    return render_to_response(
        'pars/purchase.html',
        {'gumroad_id': purchase.gumroad_id, 'pdf_url': pdf_url})

def request_sleep(request, sleep_time):
    sleeping = sleep_task.delay(int(sleep_time))
    return HttpResponse(sleeping.id)
