from django.contrib import admin
from api.models import Provider, Category, Diagnosis, DecisionTree, \
    Question, QuestionAnswer, Treatment

admin.site.register(Provider)
admin.site.register(Category)
admin.site.register(Diagnosis)
admin.site.register(DecisionTree)

admin.site.register(Question)
admin.site.register(QuestionAnswer)
admin.site.register(Treatment)
