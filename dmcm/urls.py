from django.conf.urls.defaults import patterns
from django.views.generic import DetailView, ListView
from project.dmcm.models import Page
from project.dmcm.views import search_pages, WideListView
from project.dmcm.utils import LatestBlogPostsFeed
from project.settings import SITE_ROOT_ID, BLOG_ROOT_ID

BLOG_ROOT = Page.objects.get(pk=BLOG_ROOT_ID)

urlpatterns = patterns('',
    (r'^$', DetailView.as_view(model=Page), {'pk': SITE_ROOT_ID}),
    (r'^page/%s/$' % (BLOG_ROOT_ID), ListView.as_view(queryset=Page.objects.filter(parent__exact=BLOG_ROOT).order_by('-published')[:2],
                                                      template_name='dmcm/blog_root.html')),
    (r'^page/(?P<pk>\d+)/$', DetailView.as_view(model=Page)),
    (r'^search_pages/$', search_pages),
    (r'^site_map/$', ListView.as_view(queryset=Page.objects.exclude(parent__exact=BLOG_ROOT))),
    (r'^blog/$', ListView.as_view(queryset=Page.objects.filter(parent__exact=BLOG_ROOT).order_by('-published')[:2],
                                  template_name='dmcm/blog_root.html')),
    (r'^blog/archive/$', WideListView.as_view(queryset=Page.objects.filter(parent__exact=BLOG_ROOT).order_by('-published'),
                                          template_name='dmcm/blog_archive.html')),
    (r'^blog/feed/$', LatestBlogPostsFeed()),
    (r'^(?P<slug>[-\w]+).html$', DetailView.as_view(model=Page, slug_field='slug')),
    (r'^(?P<slug>[-\w]+)[|/]$', DetailView.as_view(model=Page, slug_field='slug')),
    )