from api.models import Provider, Diagnosis
from rest_framework import serializers

class BaseProviderSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField('get_status')

    class Meta:
        model = Provider
        fields = ('slug', 'name', 'description', 'status')

class LiveProviderSerializer(BaseProviderSerializer):
    def get_status(self, obj):
        return "live"

class TestProviderSerializer(BaseProviderSerializer):
    def get_status(self, obj):
        return "test"
