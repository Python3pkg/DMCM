from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.views import login, logout
from dmcm import settings
from dmcm.cm import views as cm_views
from dmcm.cm.feeds import LatestEntriesFeed

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', cm_views.home),
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$', logout),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),
    (r'^blogadd/$', cm_views.blog_add),
    (r'^blogupdt/(\d+)/$', cm_views.blog_update),
    (r'^rss/$', LatestEntriesFeed()),
    (r'^listadd/$', cm_views.list_add),
    (r'^listupdt/(\d+)/$', cm_views.list_update),
    (r'^options/$', cm_views.options),
    (r'^pageadd/$', cm_views.page_add),
    (r'^pageupdt/(\d+)/$', cm_views.page_update),
)
