from django.conf.urls.defaults import patterns, include
from django.contrib import admin
from django.views.generic import DetailView, ListView
from dmcm.cm.models import Page
from dmcm.cm.views import search_pages
from dmcm.cm.utils import LatestBlogPostsFeed
from dmcm.settings import DEBUG, SITE_ROOT_ID, BLOG_ROOT_ID

BLOG_ROOT = Page.objects.get(pk=BLOG_ROOT_ID)

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', DetailView.as_view(model=Page), {'pk': SITE_ROOT_ID}),
    (r'^page/%s/$' % (BLOG_ROOT_ID), ListView.as_view(queryset=Page.objects.filter(parent__exact=BLOG_ROOT).order_by('-published')[:2],
                                                      template_name='cm/blog_root.html')),
    (r'^page/(?P<pk>\d+)/$', DetailView.as_view(model=Page)),
    (r'^search_pages/$', search_pages),
    (r'^site_map/$', ListView.as_view(queryset=Page.objects.exclude(parent__exact=BLOG_ROOT))),
    (r'^blog/$', ListView.as_view(queryset=Page.objects.filter(parent__exact=BLOG_ROOT).order_by('-published')[:2],
                                  template_name='cm/blog_root.html')),
    (r'^blog/archive/$', ListView.as_view(queryset=Page.objects.filter(parent__exact=BLOG_ROOT).order_by('-published'),
                                          template_name='cm/blog_archive.html')),
    (r'^blog/feed/$', LatestBlogPostsFeed()),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),
    )

if DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/ahernp/Documents/ahernp.com/site/site_media/'}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/ahernp/Documents/ahernp.com/site/'}),
        )
