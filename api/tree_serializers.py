from api.models import DecisionTree
from rest_framework import serializers

class IndividualTreeSerializer(serializers.ModelSerializer):
    version = serializers.Field(source='version')
    structure = serializers.Field(source='decision_structure')

    class Meta:
       model = DecisionTree
       fields = ('created', 'published', 'version', 'structure')
