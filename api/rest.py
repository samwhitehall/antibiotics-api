from rest_framework import generics, permissions

from api.serializers import LiveProviderSerializer
from api.models import Provider

class LiveProviderList(generics.ListCreateAPIView):
    model = Provider
    serializer_class = LiveProviderSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        '''Filter () for providers with live DecisionTreeson Python, not SQL 
        end -- as this is a computed property, not a database field'''
        return (p for p in Provider.objects.all() if p.any_live)
