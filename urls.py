from django.conf.urls import patterns, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dmcm.views import server_status_dashboard
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'admin/login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}),  # Redirect to home page on logout
    (r'^server_status/$', server_status_dashboard),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),
    (r'^', include('dmcm.urls')),
)

# When running in development mode use Django to serve the static files.
urlpatterns += staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
