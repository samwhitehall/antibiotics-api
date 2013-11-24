from api.models import DecisionTree, Question, Treatment
import api.tree_crawler as tree_crawler

from rest_framework import serializers

class IndividualTreeSerializer(serializers.ModelSerializer):
    version = serializers.Field(source='version')
    structure = serializers.Field(source='decision_structure')
    questions = serializers.SerializerMethodField('question_crawler')
    treatments = serializers.SerializerMethodField('treatment_crawler')

    def question_crawler(self, obj):
        tree = obj.decision_structure 
        qids = {q for q in tree_crawler.crawl(tree, 'q')}
        questions = Question.objects.filter(qid__in=qids)

        return QuestionSerializer(questions).data

    # DRY violation... makes me sad :(
    def treatment_crawler(self, obj):
        tree = obj.decision_structure 
        tids = {t for t in tree_crawler.crawl(tree, 't')}
        treatments = Treatment.objects.filter(tid__in=tids)

        return TreatmentSerializer(treatments).data

    class Meta:
        model = DecisionTree
        fields = ('created', 'published', 'version', 'questions', 
            'treatments', 'structure')

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
