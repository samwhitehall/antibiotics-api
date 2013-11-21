from django.http import Http404
from rest_framework import generics, permissions
from rest_framework.response import Response

from api.diagnosis_serializers import LiveTreeSerializer, TestTreeSerializer
from api.models import DecisionTree, Provider

class BaseTreeList(generics.ListCreateAPIView):
    model = DecisionTree
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        provider_slug = self.kwargs['provider']
        provider = Provider.objects.get(slug=provider_slug)
        provider_trees = DecisionTree.objects.filter(provider=provider)

        if(self.Meta.published_only):
            provider_trees = provider_trees.filter(published=True)

        diagnoses = {tree.diagnosis for tree in provider_trees}

        test_trees = []
        for diagnosis in diagnoses:
            latest = provider_trees.filter(diagnosis=diagnosis).order_by('-created')[0]
            test_trees.append(latest)

        return test_trees

class LiveTreeList(BaseTreeList):
    serializer_class = LiveTreeSerializer
    class Meta:
        published_only = True

class TestTreeList(BaseTreeList):
    serializer_class = TestTreeSerializer
    class Meta:
        published_only = False

