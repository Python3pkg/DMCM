from django.conf.urls.defaults import patterns, include
from django.contrib import admin
from django.views.generic import DetailView, ListView
from dmcm.cm.models import Page
from dmcm.cm.views import search_pages
from dmcm.settings import DEBUG, SITE_ROOT_ID

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', DetailView.as_view(model=Page), {'pk': SITE_ROOT_ID}),
    (r'^page/(?P<pk>\d+)/$', DetailView.as_view(model=Page)),
    (r'^search_pages/$', search_pages),
    (r'^site_map/$', ListView.as_view(model=Page)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),
    )

if DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/ahernp/Documents/ahernp.com/site/site_media/'}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/ahernp/Documents/ahernp.com/site/'}),
        )
