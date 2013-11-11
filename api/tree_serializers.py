from api.models import DecisionTree
from rest_framework import serializers

class TestTreeSerializer(serializers.ModelSerializer):
    version = serializers.Field(source='version')
    diagnosis = serializers.Field(source='diagnosis.slug')
    category = serializers.Field(source='diagnosis.category.slug')

    class Meta:
        model = DecisionTree
        fields = ('diagnosis', 'category', 'version', )
