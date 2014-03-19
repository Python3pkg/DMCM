from __future__ import absolute_import

from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from django.conf import settings

from dmcm.models import Page

from .utils import LatestBlogPostsFeed

BLOG_ROOT = Page.objects.get(slug=settings.BLOG_ROOT_SLUG)

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
