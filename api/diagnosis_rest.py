from django.http import Http404
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from api.tree_serializers import TestTreeSerializer, IndividualTreeSerializer
from api.models import DecisionTree, Provider, Diagnosis

class BaseTreeList(generics.ListCreateAPIView):
    model = DecisionTree
    serializer_class = TestTreeSerializer
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

class TestTreeList(BaseTreeList):
    class Meta:
        published_only = False

class LiveTreeList(BaseTreeList):
    class Meta:
        published_only = True

class IndividualTree(APIView):
    def get_object(self, provider, category, diagnosis):
        try:
            return DecisionTree.objects.filter(
                provider__slug=provider,
                diagnosis__category__slug=category,
                diagnosis__slug=diagnosis)[0]
        except DecisionTree.DoesNotExist:
            raise Http404

    def get(self, request, provider, category, diagnosis, format=None):
        tree = self.get_object(provider, category, diagnosis)
        serializer = IndividualTreeSerializer(tree)
        return Response(serializer.data)
