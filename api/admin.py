from django.contrib import admin
from api.models import Provider, Category, Diagnosis

admin.site.register(Provider)
admin.site.register(Category)
admin.site.register(Diagnosis)
admin.site.register(DecisionTree)
