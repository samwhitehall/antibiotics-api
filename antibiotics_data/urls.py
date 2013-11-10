from django.conf.urls import patterns, include, url
from rest_framework import routers

from api.rest import LiveProviderList

from django.contrib import admin
admin.autodiscover()

provider_urls = patterns('',
    url(r'^live/', LiveProviderList.as_view(), name='live-provider-list')
)

urlpatterns = patterns('',
    url(r'^providers/', include(provider_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth', include('rest_framework.urls', namespace='rest_framework'))
)
