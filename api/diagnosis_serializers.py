from api.models import DecisionTree
from rest_framework import serializers

class TestTreeSerializer(serializers.ModelSerializer):
    category = serializers.Field(source='diagnosis.category.name')
    diagnosis = serializers.Field(source='diagnosis.name')
    version = serializers.Field(source='version')

    class Meta:
        model = DecisionTree
        fields = ('category', 'diagnosis', 'version', )
