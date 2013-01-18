from django.conf.urls import patterns, url

urlpatterns = patterns('pars.views',
    url(r'^edit/(?P<par>\d+)?', 'edit', name='edit'),
    url(r'^make$', 'make', name='make'),
    url(r'^(?P<par>\d+)?', 'par', name='par'),
    )
