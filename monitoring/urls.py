from django.conf.urls import patterns, url
from monitoring.views import dashboard

urlpatterns = patterns(
    '',
    url(r'^dashboard/$', dashboard),
)
