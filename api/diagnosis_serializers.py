from api.models import Diagnosis
from rest_framework import serializers

class LiveDiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = ('name', 'category')
