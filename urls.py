from django.conf.urls.defaults import *
from django.views.generic import list_detail
from keda.views import *
import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from keda.reception import *


urlpatterns = patterns('',
    # Example:
    # (r'^keda/', include('keda.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    url(r'^$', home),
    (r'^admin/', include(admin.site.urls)),
    url(r'^test/$', test),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                     {'document_root': settings.MEDIA_ROOT}),
    url(r'^parousiologio/$', parousiologio),
    url(r'^availability/$', availability),
    url(r'^appartments/$', appartments),
    url(r'^reservations/$', reservations),
    url(r'^th/$', th),
    url(r'^damages/$', damages),
    url(r'^logistic/$', logistic),

)

