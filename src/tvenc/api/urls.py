from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^newjob/$', 'tvenc.api.views.get_newjob', name='api_get_newjob'),
    url(r'^update_status/$', 'tvenc.api.views.update_status', name='api_update_status'),
)

