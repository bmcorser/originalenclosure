from os.path import join, isfile
from subprocess import Popen
import json
import requests
from celery import task
from .models import Purchase

import xhtml2pdf.pisa as pisa

from django.conf import settings

def _link_callback(uri, rel):
    s_u = settings.STATIC_URL
    s_r = settings.STATIC_ROOT
    m_u = settings.MEDIA_URL
    m_r = settings.MEDIA_ROOT

    if uri.startswith(m_u):
        path = join(m_r, uri.replace(m_u, ''))
    elif uri.startswith(s_u):
        path = join(s_r, uri.replace(s_u, ''))

    # make sure that file exists
    if not isfile(path):
            messge = 'media URI must start with %s or %s'.format(s_u, s_m)
            raise Exception(message)
    return path

@task(name='building pdf', trail=True)
def make_pdf(purchase):
    from . import views
    html = views.par_pdf(purchase.par, purchase.uuid)
    pdf = open(purchase.pdf_path, 'w+b')
    pisa_status = pisa.CreatePDF(html,
                                 dest=pdf,
                                 link_callback=_link_callback)
    pdf.close()
    return purchase.serialise()

@task(name='rendering png', trail=True)
def make_png(purchase):
    purchase = Purchase.objects.get(uuid=purchase['uuid'])
    print(purchase.png_path)
    ghostscript_cmd = [
        'gs',
        '-sDEVICE=png16m',
        '-sOutputFile={0}'.format(purchase.png_path),
        '-r600',
        '-dDownScaleFactor=6',
        '-dQUIET',
        '-dBATCH',
        '-dNOPAUSE',
        purchase.pdf_path,
    ]
    assert Popen(ghostscript_cmd).wait() == 0
    return purchase.serialise()

@task(name='making gumroad product', trail=True)
def make_gumroad_product(purchase):
    purchase = Purchase.objects.get(uuid=purchase['uuid'])
    filter_kwargs = {
        'par': purchase.par,
        'sale__isnull': False,
    }
    purchase_count = Purchase.objects.filter(**filter_kwargs).count()
    url = 'https://api.gumroad.com/v2/products'
    data = {
        'url': purchase.pdf_url,
        'preview_url': purchase.png_url,
        'access_token': settings.GUMROAD_ACCESS_TOKEN,
        'name': '{0} ({1})'.format(purchase.par, purchase.uuid),
        'price':  (purchase_count + 1) * 100,
    }
    response = requests.post(url, data=data)
    response_dict = json.loads(response.content)
    short_url = response_dict['product']['short_url']
    purchase.gumroad_id = short_url.split('/')[-1:][0]
    purchase.save()
    return purchase.serialise()
