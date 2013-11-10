from rest_framework import generics, permissions

from api.serializers import LiveProviderSerializer
from api.models import Provider

class BaseProviderList(generics.ListCreateAPIView):
    model = Provider
    permission_classes = [
        permissions.AllowAny
    ]

class LiveProviderList(BaseProviderList):
    serializer_class = LiveProviderSerializer

    def get_queryset(self):
        '''Filter () for providers with live DecisionTreeson Python, not SQL 
        end -- as this is a computed property, not a database field'''
        return (p for p in Provider.objects.all() if p.any_live)
