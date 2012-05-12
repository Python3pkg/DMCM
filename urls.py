from django.conf.urls.defaults import patterns, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from project.dmcm.views import server_status_dashboard
from project.settings import MEDIA_URL, MEDIA_ROOT

admin.autodiscover()

urlpatterns = patterns('',
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$', logout),
    (r'^server_status/$', server_status_dashboard),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),
    (r'^', include('project.dmcm.urls')),
    )

# When running in development mode use Django to serve the static files.
urlpatterns += staticfiles_urlpatterns() + static(MEDIA_URL, document_root=MEDIA_ROOT)
