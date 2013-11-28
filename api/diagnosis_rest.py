from django.http import Http404
from rest_framework import generics, permissions
from rest_framework.response import Response

from api.diagnosis_serializers import LiveTreeSerializer, TestTreeSerializer
from api.models import DecisionTree, Provider

class BaseTreeList(generics.ListAPIView):
    model = DecisionTree

    def get_queryset(self):
        '''Return the list of only the newest decision tree for each diagnosis
        implemented by the requested provider.'''

        provider_slug = self.kwargs['provider']
        provider = Provider.objects.get(slug=provider_slug)
        trees_from_provider = DecisionTree.objects.filter(provider=provider)

        # filter to only find published decision trees, if required
        if(self.Meta.published_only):
            trees_from_provider = trees_from_provider.filter(published=True)

        # determine which diagnoses are implemented by decision trees associated
        # with this provider
        diagnoses = {tree.diagnosis for tree in trees_from_provider}

        latest_trees = []
        for diagnosis in diagnoses:
            latest = trees_from_provider \
                .filter(diagnosis=diagnosis) \
                .order_by('-created')[0]

            latest_trees.append(latest)

        return latest_trees

class LiveTreeList(BaseTreeList):
    serializer_class = LiveTreeSerializer

    class Meta:
        published_only = True

class TestTreeList(BaseTreeList):
    serializer_class = TestTreeSerializer

    class Meta:
        published_only = False
