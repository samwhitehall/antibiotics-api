from rest_framework import generics, permissions
from api.tree_serializers import TestTreeSerializer
from api.models import DecisionTree, Provider, Diagnosis

class TestTreeList(generics.ListCreateAPIView):
    model = DecisionTree
    serializer_class = TestTreeSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        provider_slug = self.kwargs['provider']
        provider = Provider.objects.get(slug=provider_slug)
        provider_trees = DecisionTree.objects.filter(provider=provider)

        test_trees = []
        for diagnosis in provider.diagnoses.all():
            latest = provider_trees.filter(diagnosis=diagnosis).order_by('-created')[0]
            test_trees.append(latest)

        return test_trees
