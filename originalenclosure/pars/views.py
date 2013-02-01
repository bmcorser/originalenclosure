#coding: utf-8
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from models import Par
from forms import ParForm, ImageForm

def par(request,par=None):
    try:
        par = Par.latest(par)
    except Par.DoesNotExist:
        return HttpResponseRedirect(reverse('par', args=['{0:04}'.format(int(par))]))
    older = par.older()
    template_dict = {
            'older':older,
            'par':par,
            'date':par.created.strftime('%A %Y'),
        }
    if par.hidden:
        template_dict['title_split'] = par.title.split(' ')
    return render_to_response(
        'par.html',
        template_dict
    )

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
        par = Par.latest(par)
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
  if request.method == 'POST':
    par = ParForm(request.POST,prefix="par")
    left = ImageForm(request.POST,prefix="left")
    right = ImageForm(request.POST,prefix="right")
    par = par.save()
    par.left = left.save()
    par.right = right.save()
    par.save()
    return HttpResponseRedirect(reverse('par'))
  else:
    par = ParForm(prefix="par",instance=None)
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

def review():
  u"✝★⚑☺♢"

