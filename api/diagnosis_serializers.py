from rest_framework import serializers
from rest_framework.reverse import reverse

from api.models import DecisionTree

class BaseTreeListingSerializer(serializers.ModelSerializer):
    category = serializers.Field(source='diagnosis.category.name')
    diagnosis = serializers.Field(source='diagnosis.name')
    version = serializers.Field(source='version')
    path = serializers.SerializerMethodField('get_tree_path')

    def get_tree_path(self, tree):
        # TODO: investigate why tree is sometimes None
        if tree:
            return reverse(self.url_name, kwargs = {
                'provider' : tree.provider.slug,
                'category' : tree.diagnosis.category.slug,
                'diagnosis' : tree.diagnosis.slug 
            })

    class Meta:
        model = DecisionTree
        fields = ('path', 'category', 'diagnosis', 'version' )

class LiveTreeSerializer(BaseTreeListingSerializer):
    url_name = 'live-individual-tree'

class TestTreeSerializer(BaseTreeListingSerializer):
    url_name = 'test-individual-tree'
