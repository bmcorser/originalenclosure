from django.conf.urls import patterns, url

urlpatterns = patterns('pars.views',
    url(r'^make$', 'make', name='make'),
    url(r'^(?P<par>\d+)?', 'par', name='par'),
    )
