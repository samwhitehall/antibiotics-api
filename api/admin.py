from django.contrib import admin
from api.models import Provider, Category, Diagnosis, DecisionTree, \
    Question, QuestionChoice, Treatment

admin.site.register(Provider)
admin.site.register(Category)
admin.site.register(Diagnosis)
admin.site.register(DecisionTree)

admin.site.register(Question)
admin.site.register(Treatment)
