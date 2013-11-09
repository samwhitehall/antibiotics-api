from django.conf.urls import patterns, include, url

from api.rest import ProviderResource
provider_resource = ProviderResource()

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^provider/', include(provider_resource.urls))
)
