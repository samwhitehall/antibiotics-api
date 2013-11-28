from django.test import TestCase
from api.models import Provider, Category, Diagnosis, DecisionTree

class DecisionTreeVersionTest(TestCase):
    fixtures = ['unittest.json']

    def test_new_tree(self):
        '''First new tree for an empty provider diagnosis should be v1'''
        new_tree = DecisionTree.objects.create(provider_id=1, diagnosis_id=1)
        self.assertEqual(new_tree.version, 1)

    def test_new_tree_shared_provider_cat(self):
        '''First new tree for an empty provider diagnosis should be v1 even if
        another tree exists which shares the provider & cat (but not diagnosis).'''
        d1 = Diagnosis.objects.create(slug='a', name='a', category_id=1)
        d2 = Diagnosis.objects.create(slug='b', name='b', category_id=1)

        tree1 = DecisionTree.objects.create(provider_id=1, diagnosis=d1)
        tree2 = DecisionTree.objects.create(provider_id=1, diagnosis=d2)

        self.assertEqual(tree1.version, 1)
        self.assertEqual(tree2.version, 1)

    def test_newer_tree_higher_version(self):
        '''If a diagnosis for a provider has two trees, the newer shold be v2'''
        tree1 = DecisionTree.objects.create(provider_id=1, diagnosis_id=1)
        self.assertEqual(tree1.version, 1)

        tree2 = DecisionTree.objects.create(provider_id=1, diagnosis_id=1)
        self.assertEqual(tree1.version, 1)
        self.assertEqual(tree2.version, 2)

    def test_published_nonpublished_trees_counted(self):
        '''Non-publushed trees should also count in version numbers.'''
        tree1 = DecisionTree.objects.create(
            provider_id=1, diagnosis_id=1, published=True)
        tree2 = DecisionTree.objects.create(provider_id=1, diagnosis_id=1)

        self.assertEqual(tree1.version, 1)
        self.assertEqual(tree2.version, 2)

class ProviderModelTest(TestCase):
    fixtures = ['unittest.json']

    def test_no_trees(self):
        '''If a provider has no trees, it should not advertise as a live provider.'''
        provider = Provider.objects.all()[0]
        self.assertFalse(provider.any_live)

    def test_some_unpublished(self):
        '''If a provider has some unpublished trees, it should not advertise as a
        live provider.'''
        provider = Provider.objects.all()[0]
        tree1 = DecisionTree.objects.create(provider_id=1, diagnosis_id=1)
        tree2 = DecisionTree.objects.create(provider_id=1, diagnosis_id=1)
        self.assertFalse(provider.any_live)

    def test_some_published_by_other_provider(self):
        '''The published status of a tree from another provider should not cause
        a provider to advertise as live.'''
        provider1 = Provider.objects.all()[0]
        provider2 = Provider.objects.create(name='a', slug='a', description='a')

        tree = DecisionTree.objects.create(provider_id=1, diagnosis_id=1, 
            published=True)
        self.assertTrue(provider1.any_live)
        self.assertFalse(provider2.any_live)

    def test_one_more_published(self):
        '''A provider should advertise as live if it has one or more published
        diagnosis implementations.'''
        provider = Provider.objects.all()[0]

        tree1 = DecisionTree.objects.create(
            provider_id=1, diagnosis_id=1, published=True)
        self.assertTrue(provider.any_live)

        tree2 = DecisionTree.objects.create(
            provider_id=1, diagnosis_id=1, published=True)
        self.assertTrue(provider.any_live)
