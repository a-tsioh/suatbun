from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import browse

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'ShuoWebJieZi.views.home', name='home'),
    # url(r'^ShuoWebJieZi/', include('ShuoWebJieZi.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^browse/$', 'browse.views.fiche'),
    url(r'^browse/get_json/(?P<charcode>\d+)/$', 'browse.views.get_json'),
    url(r'^browse/get_explanation/(?P<charcode>\d+)/$', 'browse.views.get_explanation'),
)
