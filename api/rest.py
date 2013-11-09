from rest_framework import generics, permissions

from api.serializers import ProviderSerializer
from api.models import Provider

class ProviderList(generics.ListCreateAPIView):
    model = Provider
    serializer_class = ProviderSerializer
    permission_classes = [
        permissions.AllowAny
    ]
