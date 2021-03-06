

from django.conf.urls import url

from .views import PageCreateView, PageListView, PageUpdateView

urlpatterns = [
    url(regex=r'^$',
       view=PageListView.as_view(),
       name='edit'),
    url(regex=r'^page/$',
       view=PageListView.as_view(),
       name='list_pages'),
    url(regex=r'^page/add/$',
       view=PageCreateView.as_view(),
       name='add_page'),
    url(regex=r'^(?P<slug>[-\w]+)/$',
       view=PageUpdateView.as_view(),
       name='update_page'),
]
