from django.conf.urls import patterns, url, include
from django.views.generic import DetailView, ListView
from dmcm.models import Page
from dmcm.views import search_pages, show_tool
from django.conf import settings

urlpatterns = patterns(
    '',
    url(r'^$', 
        DetailView.as_view(model=Page), 
        {'slug': settings.SITE_ROOT_SLUG}, 
        name='dmcm_root'),
    url(r'^search_pages/$', 
        search_pages, 
        name='dmcm_search_pages'),
    url(r'^site_map/$', 
        ListView.as_view(queryset=Page.objects.all()), 
        name='dmcm_site_map'),
    url(r'^tools/(?P<tool_name>[-\w]+).html$', 
        show_tool, 
        name='dmcm_show_tool_html'),
    url(r'^tools/(?P<tool_name>[-\w]+)/$', 
        show_tool, 
        name='dmcm_show_tool'),
    url(r'^dmcm/edit/', include('dmcm.edit.urls')),
    url(r'^(?P<slug>[-\w]+).html$', 
        DetailView.as_view(model=Page), 
        name='dmcm_page_detail_html'),
    url(r'^(?P<slug>[-\w]+)/$', 
        DetailView.as_view(model=Page), 
        name='dmcm_page_detail'),
)
