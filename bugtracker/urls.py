from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView, ListView
from project.dmcm.models import Page
from project.dmcm.views import edit_page, search_pages, WideListView
from project.dmcm.utils import LatestBlogPostsFeed
from project.settings import SITE_ROOT_ID, BLOG_ROOT_ID

BLOG_ROOT = Page.objects.get(pk=BLOG_ROOT_ID)

urlpatterns = patterns('',
    url(r'^$', DetailView.as_view(model=Page), {'pk': SITE_ROOT_ID}, name='dmcm_root'),
    url(r'^page/%s/$' % (BLOG_ROOT_ID),
        ListView.as_view(queryset=Page.objects.filter(parent__exact=BLOG_ROOT).order_by('-published')[:2], template_name='dmcm/blog_root.html'),
        name='dmcm_blog_root'),
    url(r'^page/(?P<pk>\d+)/$', DetailView.as_view(model=Page), name='dmcm_page_detail_id'),
    url(r'^search_pages/$', search_pages, name='dmcm_search_pages'),
    url(r'^site_map/$', ListView.as_view(queryset=Page.objects.exclude(parent__exact=BLOG_ROOT)), name='dmcm_site_map'),
    url(r'^blog/$', 
        ListView.as_view(queryset=Page.objects.filter(parent__exact=BLOG_ROOT).order_by('-published')[:2], template_name='dmcm/blog_root.html'),
        name='dmcm_blog_summary'),
    url(r'^blog/archive/$', 
        WideListView.as_view(queryset=Page.objects.filter(parent__exact=BLOG_ROOT).order_by('-published'), template_name='dmcm/blog_archive.html'),
        name='dmcm_blog_archive'),
    url(r'^blog/feed/$', LatestBlogPostsFeed(), name='dmcm_blog_feed'),
    url(r'^edit/(?P<slug>[-\w]+).html$', edit_page, name='dmcm_edit_page_html'),
    url(r'^edit/(?P<slug>[-\w]+)[|/]$', edit_page, name='dmcm_edit_page'),
    url(r'^(?P<slug>[-\w]+).html$', DetailView.as_view(model=Page, slug_field='slug'), name='dmcm_page_detail_html'),
    url(r'^(?P<slug>[-\w]+)[|/]$', DetailView.as_view(model=Page, slug_field='slug'), name='dmcm_page_detail'),
)