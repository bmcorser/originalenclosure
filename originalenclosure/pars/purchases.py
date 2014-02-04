from os.path import join, isfile
from subprocess import Popen
import json
import requests
from pars.models import Purchase

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

def make_pdf(par, uuid=None):
    from . import views
    filename = '{0}.pdf'.format(par.slug)
    if uuid:
        filename = '{0}-{1}.pdf'.format(par.slug, uuid)
    html = views.par_pdf(par, uuid)
    pdf_path = join(settings.MEDIA_ROOT, 'pars', 'purchases', filename)
    pdf = open(pdf_path, 'w+b')
    pisa_status = pisa.CreatePDF(html,
                                 dest=pdf,
                                 link_callback=_link_callback)
    pdf.close()
    return filename

def make_png(pdf_path, purchase):
    purchases_path = join(settings.MEDIA_ROOT,
                          'pars',
                          'purchases')
    outpath = join(purchases_path, '{0}.png'.format(purchase.uuid))
    ghostscript_cmd = [
        'gs',
        '-sDEVICE=png16m',
        '-sOutputFile={0}'.format(outpath),
        '-r600',
        '-dDownScaleFactor=6',
        '-dQUIET',
        '-dBATCH',
        '-dNOPAUSE',
        join(purchases_path, purchase.pdf),
    ]
    assert Popen(ghostscript_cmd).wait() == 0
    return outpath

def make_gumroad_product(purchase):
    filter_kwargs = {
        'par': purchase.par,
        'sale__isnull': False,
    }
    purchase_count = Purchase.objects.filter(**filter_kwargs).count()
    url = 'https://api.gumroad.com/v2/products'
    pdf_path = join(settings.MEDIA_ROOT, 'pars', 'purchases', purchase.pdf)
    png_path = make_png(pdf_path, purchase)
    url_components = [
        settings.DOMAIN,
        settings.MEDIA_URL.strip('/'),
        'pars',
        'purchases',
    ]
    data = {
        'url': '/'.join(url_components + [purchase.pdf]),
        'preview_url': '/'.join(url_components + ['{0}.png'.format(purchase.uuid)]),
        'access_token': settings.GUMROAD_ACCESS_TOKEN,
        'name': '{0} ({1})'.format(purchase.par, purchase.uuid),
        'price':  (purchase_count + 1) * 100,
    }
    response = requests.post(url, data=data)
    response_dict = json.loads(response.content)
    short_url = response_dict['product']['short_url']
    purchase.gumroad_id = short_url.split('/')[-1:][0]
    purchase.save()
    return purchase
