from django.conf.urls import patterns, url

urlpatterns = patterns('pars.views',
    url(r'^$', 'par', name='parhome' ),
    url(r'^swap/(?P<par>\d+)', 'swap', name='swap'),
    url(r'^edit/(?P<par>\d+)?', 'edit', name='edit'),
    url(r'^make$', 'make', name='make'),
    url(r'^par/(?P<par>\d+)', 'par', name='par'), # catch legacy urls
    url(r'^(?P<par>\d+)', 'par', name='par'),
    url(r'^permapar/(?P<slug>[\w-]+)', 'permapar', name='permapar'),
    )
