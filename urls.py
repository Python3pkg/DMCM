from django.conf.urls.defaults import patterns, include
from django.contrib import admin
from dmcm.cm.views import page
from dmcm.settings import DEBUG

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', page, {'page_id': 3}), # Homepage
    (r'^page/(\d+)/$', page),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),
    )

if DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/ahernp/Documents/ahernp.com/site/site_media/'}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/ahernp/Documents/ahernp.com/site/'}),
        )
