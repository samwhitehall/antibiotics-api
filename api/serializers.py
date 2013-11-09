from api.models import Provider
from rest_framework import serializers

class ProviderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Provider
        fields = ('slug', 'name', 'description')
