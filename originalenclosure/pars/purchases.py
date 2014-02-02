from os.path import join, isfile
from subprocess import Popen

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

def make_png(self, pdf_path):
    purchases_path = join(settings.MEDIA_ROOT,
                            'pars',
                            'purchases')
    outpath = join(purchases_path, '{0}.png'.format(self.uuid))
    ghostscript_cmd = [
        'gs',
        '-sDEVICE=png16m',
        '-sOutputFile={0}'.format(outpath),
        '-r1200',
        '-dDownScaleFactor=6',
        '-dQUIET',
        '-dBATCH',
        '-dNOPAUSE',
        join(purchases_path, self.uuid),
    ]
    assert Popen(ghostscript_cmd).wait() == 0
    return outpath

def make_gumroad_product(self):
    from ipdb import set_trace;set_trace()
    url = 'https://api.gumroad.com/v2/products'
    pdf_path, err = self.make_pdf()
    png_path = self.make_png(pdf_path)
    url_components = [
        settings.DOMAIN,
        settings.MEDIA_URL.strip('/'),
        'pars',
        'purchases',
    ]
    data = {
        'url': '/'.join(url_components + [self.uuid]),
        'preview_url': '/'.join(url_components + ['{0}.png'.format(self.uuid)]),
        'access_token': settings.GUMROAD_ACCESS_TOKEN,
        'name': '{0} ({1})'.format(self.par, self.uuid),
        'price': 100,
    }
    response = requests.post(url, data=data)
    response_dict = json.loads(response.content)
    self.gumroad_id = response_dict['product']['id']
    self.save()
    return response

