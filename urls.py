from django.conf.urls.defaults import patterns, include
from django.contrib import admin
from django.contrib.auth.views import login, logout
from project.dmcm.views import server_status_dashboard
from project.settings import DEVELOP

admin.autodiscover()

urlpatterns = patterns('',
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$', logout),
    (r'^server_status/$', server_status_dashboard),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),
    (r'^', include('project.dmcm.urls')),
    )

if DEVELOP:
    # When running in development mode use Django to server the static files.
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/ahernp/Documents/ahernp.com/site/site_media/'}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/ahernp/Documents/ahernp.com/site/'}),
        )
