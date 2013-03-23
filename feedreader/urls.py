from django.conf.urls import patterns, url
from feedreader.views import feeds, ajax_get_feeds, ajax_get_num_unread

urlpatterns = patterns(
    '',
    url(r'^$', feeds),
    url(r'^get_feeds/$', ajax_get_feeds),
    url(r'^get_num_unread/$', ajax_get_num_unread),
)
