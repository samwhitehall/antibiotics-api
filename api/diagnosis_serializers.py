from rest_framework import serializers
from rest_framework.reverse import reverse

from api.models import DecisionTree

class BaseTreeListingSerializer(serializers.ModelSerializer):
    category = serializers.Field(source='diagnosis.category.name')
    diagnosis = serializers.Field(source='diagnosis.name')
    version = serializers.Field(source='version')
    path = serializers.SerializerMethodField('get_tree_path')

    class Meta:
        model = DecisionTree
        fields = ('path', 'category', 'diagnosis', 'version' )

class LiveTreeSerializer(BaseTreeListingSerializer):
    def get_tree_path(self, tree):
        # TODO: investigate why tree is sometimes None
        if tree:
            provider_slug = tree.provider.slug
            category_slug = tree.diagnosis.category.slug
            diagnosis_slug = tree.diagnosis.slug

            return reverse('live-individual-tree', kwargs = {
                'provider' : provider_slug,
                'category' : category_slug,
                'diagnosis' : diagnosis_slug
            })

class TestTreeSerializer(BaseTreeListingSerializer):
    def get_tree_path(self, tree):
       return 'test' 

