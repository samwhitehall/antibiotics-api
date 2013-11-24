# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'DecisionTree.diagnosis'
        db.add_column(u'api_decisiontree', 'diagnosis',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Diagnosis'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'DecisionTree.diagnosis'
        db.delete_column(u'api_decisiontree', 'diagnosis_id')


    models = {
        u'api.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'api.decisiontree': {
            'Meta': {'object_name': 'DecisionTree'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'diagnosis': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.Diagnosis']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.Provider']", 'null': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_number': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'})
        },
        u'api.diagnosis': {
            'Meta': {'object_name': 'Diagnosis'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.Category']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'api.provider': {
            'Meta': {'object_name': 'Provider'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'diagnosis': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['api.Diagnosis']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['api']