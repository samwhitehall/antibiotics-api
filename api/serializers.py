from api.models import Provider
from rest_framework import serializers

class LiveProviderSerializer(serializers.ModelSerializer):
    def get_status(self, model):
        return "live"

    status = serializers.SerializerMethodField('get_status')

    class Meta:
        model = Provider
        fields = ('slug', 'name', 'description', 'status')
