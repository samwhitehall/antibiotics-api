from api.models import DecisionTree, Question, Treatment
import api.tree_crawler as tree_crawler

from rest_framework import serializers

class IndividualTreeSerializer(serializers.ModelSerializer):
    version = serializers.Field(source='version')
    structure = serializers.Field(source='decision_structure')
    questions = serializers.SerializerMethodField('question_crawler')

    def question_crawler(self, obj):
        tree = obj.decision_structure 
        qids = {x for x in tree_crawler.crawl(tree, 'q')}
        questions = Question.objects.filter(qid__in=qids)
        return QuestionSerializer(questions).data

    class Meta:
        model = DecisionTree
        fields = ('created', 'published', 'version', 
            'questions', 'structure')

class QuestionSerializer(serializers.ModelSerializer):
    text = serializers.Field(source='label')
    info = serializers.Field(source='information')

    class Meta:
        model = Question
        fields = ('qid', 'text', 'info')
