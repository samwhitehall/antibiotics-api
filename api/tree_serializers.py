from api.models import DecisionTree
from rest_framework import serializers

class TestTreeSerializer(serializers.ModelSerializer):
    version = serializers.Field(source='version')

    class Meta:
        model = DecisionTree
        fields = ('created', 'version', 'published', 'diagnosis')
