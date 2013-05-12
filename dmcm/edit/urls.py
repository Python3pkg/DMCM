from django.conf.urls import patterns, url
from django.views.generic import ListView
from dmcm.edit.views import PageCreateView, PageUpdateView
from dmcm.models import Page

urlpatterns = patterns(
    '',
    url(r'^$', 
        ListView.as_view(
            model=Page,
            template_name='dmcm/edit/page_list.html'), 
        name='dmcm_edit'),
    url(r'^page/$', 
        ListView.as_view(
            model=Page,
            template_name='dmcm/edit/page_list.html'), 
        name='dmcm_edit_list_pages'),
     url(r'^page/add/$', 
        PageCreateView.as_view(), 
         name='dmcm_edit_add_page'),
    url(r'^(?P<slug>[-\w]+)/$', 
        PageUpdateView.as_view(), 
        name='dmcm_edit_update_page'),
)
