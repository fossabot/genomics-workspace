from datetime import datetime
from django.conf.urls import patterns, include, url
from app.forms import BootstrapAuthenticationForm
from userprofile.forms import BootStrapPasswordChangeForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.sites.models import Site
admin.autodiscover()
#admin.site.unregister(Site)

#from filebrowser.sites import site

urlpatterns = patterns('',
    # Examples:
    url(r'^home$', 'app.views.home', name='home'),
    #url(r'^contact$', 'app.views.contact', name='contact'),
    url(r'^about', 'app.views.about', name='about'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/filebrowser/', include('filebrowser.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls'), name='doc'),
    url(r'^proxy/', include('proxy.urls', namespace='proxy')),
    url(r'^user/', include('userprofile.urls', namespace='userprofile')),
    url(r'^webapollo/', include('webapollo.urls', namespace='webapollo')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # BLAST
    url(r'^blast/', include('blast.urls', namespace='blast')),
)
from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
    )
