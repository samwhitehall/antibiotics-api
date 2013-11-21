from django.conf.urls import patterns, include, url
from rest_framework import routers

from api.provider_rest import LiveProviderList, TestProviderList
from api.diagnosis_rest import LiveTreeList, TestTreeList
from api.tree_rest import LiveIndividualTree, TestIndividualTree, \
    SpecificIndividualTree

from django.contrib import admin
admin.autodiscover()

provider_urls = patterns('',
    url(r'^test', TestProviderList.as_view(), name='test-provider-list'),
    url(r'(?:live)?$', LiveProviderList.as_view(), name='live-provider-list')
)

tree_list_urls = patterns('',
    url(r'^test', TestTreeList.as_view(), name='test-tree-list'),
    url(r'^(?:live)?$', LiveTreeList.as_view(), name='live-tree-list'),
)

tree_urls = patterns('',
    url(r'^test', TestIndividualTree.as_view(), name='test-individual-tree'),
    url(r'^(?:live)?$', LiveIndividualTree.as_view(), name='live-individual-tree'),
    url(r'^(?P<version>[0-9]+)?$', SpecificIndividualTree.as_view(), 
        name='specific-individual-tree'),
)

diagnosis_urls = patterns('',
    url(r'^tree/' \
            '(?P<provider>[a-z-]+)/' \
            '(?P<category>[a-z-]+)/' \
            '(?P<diagnosis>[a-z-]+)/', include(tree_urls)),
    url(r'^(?P<provider>[a-z]+)/', include(tree_list_urls))
)

urlpatterns = patterns('',
    url(r'^providers/', include(provider_urls)),
    url(r'^data/', include(diagnosis_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth', include('rest_framework.urls', namespace='rest_framework'))
)
