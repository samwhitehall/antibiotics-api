from api.models import DecisionTree
from rest_framework import serializers

class IndividualTreeSerializer(serializers.ModelSerializer):
    class Meta:
       model = DecisionTree
       fields = ('created', 'published')
