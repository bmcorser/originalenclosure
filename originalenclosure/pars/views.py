from django.shortcuts import render_to_response
from models import Par

def par_home(request):
  return render_to_response(
      'pars_home.html',
      {}
      )

def par_page(request,par):
  par = Par.objects.get(id=par)
  return render_to_response(
      'par_page.html',
      {'par':par}
      )
