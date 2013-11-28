from django.test import TestCase, Client
from api.models import Provider, Category, Diagnosis, DecisionTree

import simplejson as json

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

class ProviderListViewTest(TestCase):
    fixtures = ['providers.json', 'categories.json', 'diagnoses.json', 
        'questions.json', 'treatments.json', 'trees.json']

    def setUp(self):
        live_response = Client().get('/providers/')
        self.assertEqual(live_response.status_code, 200)
        self.live_content = json.loads(live_response.content)

        test_response = Client().get('/providers/test')
        self.assertEqual(test_response.status_code, 200)
        self.test_content = json.loads(test_response.content)

    def test_live_contains_suht(self):
        self.assertEqual(self.live_content[0]['slug'], 'suht')

    def test_live_contains_correct_fields(self):
        self.assertIn('name', self.live_content[0].keys())
        self.assertIn('description', self.live_content[0].keys())
        self.assertEquals(self.live_content[0]['status'], 'live')

    def test_test_contains_suht_phnt(self):
        self.assertEqual(self.test_content[0]['slug'], 'suht')
        self.assertEqual(self.test_content[1]['slug'], 'phnt')

    def test_test_contains_correct_fields(self):
        self.assertSetEqual(set(self.test_content[0].keys()), 
            {'slug', 'name', 'description', 'status'})

        self.assertEqual(self.test_content[0]['status'], 'test')
        self.assertEqual(self.test_content[1]['status'], 'test')

    def test_default_url_is_live_url(self):
        live = Client().get('/providers/live')
        self.assertEqual(live.status_code, 200)

        content = json.loads(live.content)
        self.assertEqual(content, self.live_content)

    def test_add_provider_no_published(self):
        slug = 'our-slug'
        name = 'Provider'
        description = 'abc123'
        new_provider = Provider.objects.create(
            slug=slug, name=name, description=description)

        self.setUp()
        self.assertEqual(len(self.test_content), 3)
        self.assertEqual(self.test_content[2]['slug'], slug)
        self.assertEqual(self.test_content[2]['name'], name)
        self.assertEqual(self.test_content[2]['description'], description)
        self.assertEqual(len(self.live_content), 1)

    def test_add_provider_published(self):
        slug = 'our-slug'
        name = 'Provider'
        description = 'abc123'
        new_provider = Provider.objects.create(
            slug=slug, name=name, description=description)
        tree1 = DecisionTree.objects.create(
            provider_id=3, diagnosis_id=1, published=True)

        self.setUp()

        self.assertEqual(len(self.test_content), 3)
        self.assertEqual(self.test_content[2]['slug'], slug)
        self.assertEqual(self.test_content[2]['name'], name)
        self.assertEqual(self.test_content[2]['description'], description)

        self.assertEqual(len(self.live_content), 2)
        self.assertEqual(self.live_content[1]['slug'], slug)
        self.assertEqual(self.live_content[1]['name'], name)
        self.assertEqual(self.live_content[1]['description'], description)

class DiagnosisListViewTest(TestCase):
    fixtures = ['providers.json', 'categories.json', 'diagnoses.json', 
       'questions.json', 'treatments.json', 'trees.json']

    def setUp(self):
        live_response = Client().get('/data/suht/')
        self.assertEqual(live_response.status_code, 200)
        self.live_content = json.loads(live_response.content)

        test_response = Client().get('/data/suht/test')
        self.assertEqual(test_response.status_code, 200)
        self.test_content = json.loads(test_response.content)

    def test_live_contains_correct_fields(self):
        self.assertSetEqual(set(self.live_content[0].keys()),
            {'path', 'category', 'diagnosis', 'version'})

    def test_live_all_slugs_valid(self):
        for diagnosis in self.live_content:
            res = Client().get(diagnosis['path'])
            self.assertEqual(res.status_code, 200)

    def test_test_contains_correct_fields(self):
        self.assertSetEqual(set(self.test_content[0].keys()),
            {'path', 'category', 'diagnosis', 'version'})

    def test_test_all_slugs_valid(self):
        for diagnosis in self.test_content:
            res = Client().get(diagnosis['path'])
            self.assertEqual(res.status_code, 200)

    def test_default_url_is_live_url(self):
        live = Client().get('/data/suht/live')
        self.assertEqual(live.status_code, 200)

        content = json.loads(live.content)
        self.assertEqual(content, self.live_content)

    def test_add_new_diagnosis_no_implementation(self):
        slug = 'diagnosis-slug'
        name = 'My Diagnosis'
        new_diagnosis = Diagnosis.objects.create(
            slug=slug, name=name, category_id=1)

        self.setUp()

        self.assertEqual(len(self.live_content), 2)
        self.assertEqual(len(self.test_content), 3)

    def test_add_new_unpublished_diagnosis_implementation(self):
        slug = 'diagnosis-slug'
        name = 'My Diagnosis'
        new_diagnosis = Diagnosis.objects.create(
            slug=slug, name=name, category_id=1)
        tree = DecisionTree.objects.create(
            provider_id=1, diagnosis_id=new_diagnosis.id)

        self.setUp()

        self.assertEqual(len(self.live_content), 2)
        self.assertEqual(len(self.test_content), 4)
        self.assertEqual(self.test_content[3]['diagnosis'], name)

    def test_add_new_published_diagnosis_implementation(self):
        slug = 'diagnosis-slug'
        name = 'My Diagnosis'
        new_diagnosis = Diagnosis.objects.create(
            slug=slug, name=name, category_id=1)
        tree = DecisionTree.objects.create(
            provider_id=1, diagnosis_id=new_diagnosis.id, published=True)

        self.setUp()

        self.assertEqual(len(self.live_content), 3)
        self.assertEqual(len(self.test_content), 4)
        self.assertEqual(self.live_content[2]['diagnosis'], name)
        self.assertEqual(self.test_content[3]['diagnosis'], name)

class IndividualTreeViewTest(TestCase):
    fixtures = ['providers.json', 'categories.json', 'diagnoses.json', 
        'questions.json', 'treatments.json', 'trees.json']

    def setUp(self):
        response = Client().get('/data/tree/suht/respiratory/pneumonia/')
        self.assertEqual(response.status_code, 200)
        self.content = json.loads(response.content)

    def test_contains_correct_root_fields(self):
        self.assertSetEqual(set(self.content[0].keys()),
            {'published', 'created', 'version', 'questions', 
             'treatments', 'structure'})

    def test_contains_correct_questions(self):
        qids = {question['qid'] for question in self.content[0]['questions']}
        self.assertSetEqual(qids, {'lcon', 'cacq', 'c65s', 'pall', 'toma', 'hcopd'})

    def test_contains_correct_treatments(self):
        tids = {treatment['tid'] for treatment in self.content[0]['treatments']}
        self.assertSetEqual(tids, {'opt%d' % i for i in range(1,len(tids)+1)})

    def test_specify_exact_version_is_same(self):
        self.assertEqual(self.content[0]['version'], 1)

    def test_conforms_to_schema(self):
        self.assertTrue(False)

    def test_add_remove_question_to_tree(self):
        self.assertTrue(False)

    def test_add_remove_treatment_to_tree(self):
        self.assertTrue(False)

class EmptyIndividualTreeViewTest(TestCase):
    fixtures = ['providers.json', 'categories.json', 'diagnoses.json', 
        'questions.json', 'treatments.json', 'trees.json']

    def setUp(self):
        response = Client().get('/data/tree/suht/urinary/uti/')
        self.assertEqual(response.status_code, 200)
        self.content = json.loads(response.content)

    def test_contains_correct_root_fields(self):
        self.assertSetEqual(set(self.content[0].keys()),
            {'published', 'created', 'version', 'questions', 
             'treatments', 'structure'})

    def test_contains_empty_questions(self):
        self.assertEqual(self.content[0]['questions'], [])

    def test_contains_empty_treatments(self):
        self.assertEqual(self.content[0]['treatments'], [])

    def test_contains_empty_structure(self):
        self.assertEqual(self.content[0]['structure'], [])
