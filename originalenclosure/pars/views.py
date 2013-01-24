from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Par
from forms import ParForm, ImageForm

def par(request,par):
  pars = Par.objects.all()
  pages = Paginator(pars,1)
  try:
    page = pages.page(par)
  except (PageNotAnInteger, EmptyPage):
    page = pages.page(pages.num_pages)
  par = page.object_list[0]
  template_dict = {
        'page':page,
        'par':par,
        'date':par.created.strftime('%A %Y'),
      }
  if par.hidden:
    template_dict['title_split'] = par.title.split(' ')
  return render_to_response(
      'par.html',
      template_dict
    )

def edit(request,par):
  pars = Par.objects.all()
  pages = Paginator(pars,1)
  try:
    page = pages.page(par)
  except (PageNotAnInteger, EmptyPage):
    page = pages.page(pages.num_pages)
  par = page.object_list[0]
  if request.method == 'POST':
    par_form = ParForm(request.POST,instance=par,prefix="par").save()
    left = ImageForm(request.POST,instance=par.left,prefix="left").save()
    right = ImageForm(request.POST,instance=par.right,prefix="right").save()
  par_form = ParForm(prefix="par",instance=par)
  left_form = ImageForm(prefix="left",instance=par.left)
  right_form = ImageForm(prefix="right",instance=par.right)
  return render_to_response("edit.html", {
    "page":page,
    "par":par,
    "par_form":par_form,
    "left_form":left_form,
    "right_form":right_form,
  },
    context_instance=RequestContext(request))

def make(request):
  if request.method == 'POST':
    par = ParForm(request.POST,prefix="par")
    left = ImageForm(request.POST,prefix="left")
    right = ImageForm(request.POST,prefix="right")
    par = par.save()
    par.left = left.save()
    par.right = right.save()
    par.save()
    return HttpResponseRedirect(reverse('pars'))
  else:
    par = ParForm(prefix="par",instance=None)
    left = ImageForm(prefix="left",instance=None)
    right = ImageForm(prefix="right",instance=None)
    return render_to_response("make.html", {
      "par":par,
      "left":left,
      "right":right,
    },
    context_instance=RequestContext(request))
