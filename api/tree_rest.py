from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response

from api.tree_serializers import IndividualTreeSerializer
from api.models import DecisionTree

class BaseIndividualTree(APIView):
    def get_object(self, provider, category, diagnosis):
        try:
            return DecisionTree.objects.filter(
                provider__slug=provider,
                diagnosis__category__slug=category,
                diagnosis__slug=diagnosis,
                published=self.Meta.published)[0]
        except DecisionTree.DoesNotExist:
            raise Http404

    def get(self, request, provider, category, diagnosis, format=None):
        tree = self.get_object(provider, category, diagnosis)
        serializer = IndividualTreeSerializer(tree)
        return Response(serializer.data)

class LiveIndividualTree(BaseIndividualTree):
    class Meta:
        published = True

class TestIndividualTree(BaseIndividualTree):
    class Meta:
        published = False
