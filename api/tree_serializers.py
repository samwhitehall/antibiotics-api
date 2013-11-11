from api.models import DecisionTree
from rest_framework import serializers

class TestTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DecisionTree
        fields = ('created', 'version_number', 'published', 'diagnosis')
