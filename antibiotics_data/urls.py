from django.conf.urls import patterns, include, url
from rest_framework import routers

from api.provider_rest import LiveProviderList, TestProviderList
from api.diagnosis_rest import LiveTreeList, TestTreeList
from api.tree_rest import IndividualTree

from django.contrib import admin
admin.autodiscover()

provider_urls = patterns('',
    url(r'^live/', LiveProviderList.as_view(), name='live-provider-list'),
    url(r'^test/', TestProviderList.as_view(), name='test-provider-list')
)

tree_urls = patterns('',
    url(r'^/live', IndividualTree.as_view(), name='live-individual-tree'),
)

diagnosis_urls = patterns('',
    url(r'^(?P<provider>[a-z]+)/live$', LiveTreeList.as_view(), name='live-tree-list'),
    url(r'^(?P<provider>[a-z]+)/test$', TestTreeList.as_view(), name='test-tree-list'),
    url(r'^tree/' \
            '(?P<provider>[a-z-]+)/' \
            '(?P<category>[a-z-]+)/' \
            '(?P<diagnosis>[a-z-]+)', include(tree_urls))
)


urlpatterns = patterns('',
    url(r'^providers/', include(provider_urls)),
    url(r'^data/', include(diagnosis_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth', include('rest_framework.urls', namespace='rest_framework'))
)
