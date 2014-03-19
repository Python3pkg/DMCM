from __future__ import absolute_import

from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, url
from django.views.generic import ListView

from ..edit.views import PageCreateView, PageUpdateView
from ..models import Page

urlpatterns = patterns(
    '',
    url(r'^$', 
        login_required(ListView.as_view(
            model=Page,
            template_name='dmcm/edit/page_list.html')), 
        name='dmcm_edit'),
    url(r'^page/$', 
        login_required(ListView.as_view(
            model=Page,
            template_name='dmcm/edit/page_list.html')), 
        name='dmcm_edit_list_pages'),
     url(r'^page/add/$', 
        login_required(PageCreateView.as_view()), 
         name='dmcm_edit_add_page'),
    url(r'^(?P<slug>[-\w]+)/$', 
        login_required(PageUpdateView.as_view()), 
        name='dmcm_edit_update_page'),
)
