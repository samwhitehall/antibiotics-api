from api.models import DecisionTree, Question, Treatment
import api.tree_crawler as tree_crawler

from rest_framework import serializers

class IndividualTreeSerializer(serializers.ModelSerializer):
    dataVersion = serializers.Field(source='version')
    schemaVersion = serializers.Field(source='version')
    DecisionTree = serializers.SerializerMethodField('question_check')
    Questions = serializers.SerializerMethodField('question_crawler')
    Treatments = serializers.SerializerMethodField('treatment_crawler')

    def schema_version(self, obj):
        '''kludge!'''
        return 1

    def question_check(self, obj):
        '''Return [] instead of 'null' string if this field is blank'''
        return obj.decision_structure or []

    def question_crawler(self, obj):
        '''Crawl the tree, find the question IDs it references, query the database
        for the questions behind this, and output a 'legend' in the API.'''
        tree = obj.decision_structure 
        if tree == None:
            return []
        qids = {q for q in tree_crawler.crawl(tree, 'q')}
        questions = Question.objects.filter(qid__in=qids)

        return QuestionSerializer(questions).data

    # DRY violation... makes me sad :(
    def treatment_crawler(self, obj):
        '''Same as question_crawler but for treatments.'''
        tree = obj.decision_structure 
        if tree == None:
            return []
        tids = {t for t in tree_crawler.crawl(tree, 't')}
        treatments = Treatment.objects.filter(tid__in=tids)

        return TreatmentSerializer(treatments).data

    class Meta: 
        model = DecisionTree 
        fields = ('created', 'published', 'dataVersion', 'schemaVersion',
        'Questions', 'Treatments', 'DecisionTree')

class QuestionSerializer(serializers.ModelSerializer):
    text = serializers.Field(source='label')
    info = serializers.Field(source='information')
    ans = serializers.Field(source='answers')
    button = serializers.Field(source='question_type')

    class Meta:
        model = Question
        fields = ('qid', 'text', 'info', 'ans', 'button')

class TreatmentSerializer(serializers.ModelSerializer):
    desc = serializers.Field(source='details')

    class Meta:
        model = Treatment
        fields = ('tid', 'desc')
