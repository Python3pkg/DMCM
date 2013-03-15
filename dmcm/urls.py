from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from dmcm.models import Page
from dmcm.views import edit_page, search_pages, show_tool, WideListView
from dmcm.utils import LatestBlogPostsFeed
from django.conf import settings

BLOG_ROOT = Page.objects.get(pk=settings.BLOG_ROOT_ID)

urlpatterns = patterns(
    '',
    url(r'^$', DetailView.as_view(model=Page), {'pk': settings.SITE_ROOT_ID}, name='dmcm_root'),
    url(r'^search_pages/$', search_pages, name='dmcm_search_pages'),
    url(r'^site_map/$', ListView.as_view(queryset=Page.objects.exclude(parent__exact=BLOG_ROOT)), name='dmcm_site_map'),
    url(r'^blog/$',
        ListView.as_view(queryset=Page.objects.filter(parent__exact=BLOG_ROOT).order_by('-published')[:2], template_name='dmcm/blog_root.html'),
        name='dmcm_blog_summary'),
    url(r'^blog/archive/$',
        WideListView.as_view(queryset=Page.objects.filter(parent__exact=BLOG_ROOT).order_by('-published'), template_name='dmcm/blog_archive.html'),
        name='dmcm_blog_archive'),
    url(r'^blog/feed/$', LatestBlogPostsFeed(), name='dmcm_blog_feed'),
    url(r'^tools/(?P<tool_name>[-\w]+).html$', show_tool, name='dmcm_show_tool_html'),
    url(r'^tools/(?P<tool_name>[-\w]+)[|/]$', show_tool, name='dmcm_show_tool'),
    url(r'^edit/(?P<slug>[-\w]+).html$', edit_page, name='dmcm_edit_page_html'),
    url(r'^edit/(?P<slug>[-\w]+)[|/]$', edit_page, name='dmcm_edit_page'),
    url(r'^(?P<slug>[-\w]+).html$', DetailView.as_view(model=Page, slug_field='slug'), name='dmcm_page_detail_html'),
    url(r'^(?P<slug>[-\w]+)[|/]$', DetailView.as_view(model=Page, slug_field='slug'), name='dmcm_page_detail'),
)
