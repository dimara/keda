from django.conf.urls.defaults import *
from django.views.generic import list_detail
from reception.views import *
from django.conf import settings


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
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^$', home),
    (r'^admin/', include(admin.site.urls)),
    url(r'^test/$', test),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                     {'document_root': settings.STATIC_ROOT}),
    url(r'^parousiologio/$', parousiologio),
    url(r'^availability/$', availability),
    url(r'^appartments/$', appartments),
    url(r'^reservations/$', reservations),
    url(r'^th/$', th),
    url(r'^damages/$', damages),
    url(r'^logistic/$', logistic),
    url(r'^gmap/$', gmap),
    url(r'^gmap_data/$', gmap_data),
    url(r'^info/$', info),
    url(r'^lookup/$', lookup),
    url(r'^stats/$', stats),
    url(r'^graphs/$', send_file),

)

