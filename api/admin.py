from django.contrib import admin
from api.models import Provider, Category, Diagnosis, DecisionTree, \
    Question, Treatment

admin.site.register(Provider)
admin.site.register(Category)
admin.site.register(Diagnosis)

admin.site.register(Question)
admin.site.register(Treatment)

class DecisionTreeAdmin(admin.ModelAdmin):
    model = DecisionTree
    view_on_site = True
    list_display = ('diagnosis', 'provider', 'version',)
    fields = ('published', 'version', 'provider', 'diagnosis', 'decision_structure')

    def get_readonly_fields(self, req, obj=None):
        if obj: # in edit mode
            return ('created', 'provider', 'diagnosis', 'version', 'decision_structure')
        return ('version', 'created')

admin.site.register(DecisionTree, DecisionTreeAdmin)
