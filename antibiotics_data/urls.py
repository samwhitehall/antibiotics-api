from django.conf.urls import patterns, include, url
from rest_framework import routers

from api.provider_rest import LiveProviderList, TestProviderList
from api.diagnosis_rest import LiveDiagnosisList

from django.contrib import admin
admin.autodiscover()

provider_urls = patterns('',
    url(r'^live/', LiveProviderList.as_view(), name='live-provider-list'),
    url(r'^test/', TestProviderList.as_view(), name='test-provider-list')
)

data_urls = patterns('',
    url(r'^(?P<slug>[a-z]+)$', LiveDiagnosisList.as_view(), name='live-diagnosis-list'),
)

urlpatterns = patterns('',
    url(r'^providers/', include(provider_urls)),
    url(r'^data/', include(data_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth', include('rest_framework.urls', namespace='rest_framework'))
)
