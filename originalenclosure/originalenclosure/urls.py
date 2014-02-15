from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import direct_to_template
admin.autodiscover()

urlpatterns = patterns('',
    # static pages
    url(
        r'^$',
        direct_to_template,
        {'template':'home.html'},
        name='home'),
    url(r'^robots.txt$',
        direct_to_template,
        {'template':'robots.txt'},
        name='home'),
    url(
        r'^mcfp/$', direct_to_template, {'template':'home.html'}, name='home'),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to',
        {'url': '/static/favicon.ico'}),

    # admin / login
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^admin/', include(admin.site.urls)),

    # apps
    url(r'^pars/', include('pars.urls')),

    # plugins
    url(r'^djangojs/', include('djangojs.urls')),

)

if settings.DEBUG:
  urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
     'document_root': settings.MEDIA_ROOT}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
     'document_root': settings.STATIC_ROOT}))
