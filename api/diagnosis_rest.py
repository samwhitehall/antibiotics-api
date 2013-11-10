from rest_framework import generics, permissions
from api.diagnosis_serializers import LiveDiagnosisSerializer
from api.models import Diagnosis, Provider

class LiveDiagnosisList(generics.ListCreateAPIView):
    serializer_class = LiveDiagnosisSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        slug = self.kwargs['slug']
        provider = Provider.objects.get(slug=slug)
        return provider.diagnoses.all()
