from django.contrib import admin
from api.models import Provider, Category, Diagnosis, DecisionTree, \
    Question, Treatment

admin.site.register(Provider)
admin.site.register(Category)
admin.site.register(Diagnosis)

admin.site.register(Question)
admin.site.register(Treatment)

class DecisionTreeAdmin(admin.ModelAdmin):
    def visualise(self, obj):
        return '<a href="%s">%s</a>' % (obj.visualisation_link, obj)
    visualise.allow_tags = True

    model = DecisionTree
    list_display = ('diagnosis', 'provider', 'version', 'visualise')
    fields = ('published', 'version', 'provider', 'diagnosis', 
        'decision_structure', 'visualise')
    
    def get_readonly_fields(self, req, obj=None):
        if obj: # in edit mode
            return ('created', 'provider', 'diagnosis', 'version', 
                'decision_structure', 'visualise')

        return ('version', 'created', 'visualise')


admin.site.register(DecisionTree, DecisionTreeAdmin)
