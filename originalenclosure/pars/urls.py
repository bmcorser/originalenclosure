from django.conf.urls import patterns, url

urlpatterns = patterns('pars.views',
    url(r'^$', 'par_home', name='par_home'),
    url(r'^(?P<par>\d+)', 'par_page', name='par_page'),
    )
