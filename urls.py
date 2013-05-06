from django.conf.urls.defaults import *
from keda.views import *
import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^keda/', include('keda.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    url(r'^$', home),
    url(r'^military_persons/$', military_persons),
    (r'^admin/', include(admin.site.urls)),
    url(r'^test/$', test),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                     {'document_root': settings.MEDIA_ROOT}),
    url(r'^search/$', search),



)

