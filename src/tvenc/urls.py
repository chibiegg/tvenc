from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'tvenc.views.index', name='index'),
    url(r'^recorded/$', 'tvenc.views.list_recorded', name='list_recorded'),
    url(r'^api/', include('tvenc.api.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
