from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from dmcm.models import Page
from blog.utils import LatestBlogPostsFeed
from django.conf import settings

BLOG_ROOT = Page.objects.get(pk=settings.BLOG_ROOT_ID)

urlpatterns = patterns(
    '',
    url(r'^$',
        ListView.as_view(
            queryset=Page.objects.filter(parent__exact=BLOG_ROOT).order_by('-published')[:2], 
            template_name='blog/root.html'),
        name='blog_root'),
    url(r'^archive/$',
        ListView.as_view(
            queryset=Page.objects.filter(parent__exact=BLOG_ROOT).order_by('-published'), 
            template_name='blog/archive.html'),
        name='blog_archive'),
    url(r'^feed/$', LatestBlogPostsFeed(), 
        name='blog_feed'),
#     url(r'^edit/(?P<slug>[-\w]+).html$', 
#         edit_page, 
#         name='blog_edit_emtry_html'),
#     url(r'^edit/(?P<slug>[-\w]+)[|/]$', 
#         edit_page, 
#         name='dmcm_edit_page'),
    url(r'^(?P<slug>[-\w]+).html$', 
        DetailView.as_view(
            model=Page, 
            slug_field='slug',
            template_name='blog/entry.html'), 
        name='blog_entry_html'),
    url(r'^(?P<slug>[-\w]+)[|/]$', 
        DetailView.as_view(
            model=Page, 
            slug_field='slug',
            template_name='blog/entry.html'), 
        name='blog_entry'),
)
