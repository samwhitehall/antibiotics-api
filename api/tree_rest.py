from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response

from api.tree_serializers import IndividualTreeSerializer
from api.models import DecisionTree

class BaseIndividualTree(APIView):
    def get_trees(self, provider, category, diagnosis):
        query = DecisionTree.objects.filter(
            provider__slug=provider,
            diagnosis__category__slug=category,
            diagnosis__slug=diagnosis,
        )

        if self.Meta.published:
            query = query.filter(published=True)

        return query

    def get(self, request, provider, category, diagnosis):
        matching_trees = self.get_trees(provider, category, diagnosis)
        tree = self.single_tree(matching_trees)

        serializer = IndividualTreeSerializer(tree)
        return Response(serializer.data)

class BaseLatestIndividualTree(BaseIndividualTree):
    def single_tree(self, query):
        try:
            # TODO: work out why this is sometimes None
            if query:
                return query.order_by('published')[0:1]
        except DecisionTree.DoesNotExist:
            raise Http404

class LiveIndividualTree(BaseLatestIndividualTree):
    class Meta:
        published = True

class TestIndividualTree(BaseLatestIndividualTree):
    class Meta:
        published = False

class SpecificIndividualTree:
    pass
