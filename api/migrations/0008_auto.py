# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field diagnosis on 'Provider'
        db.delete_table(db.shorten_name(u'api_provider_diagnosis'))

        # Adding M2M table for field diagnoses on 'Provider'
        m2m_table_name = db.shorten_name(u'api_provider_diagnoses')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('provider', models.ForeignKey(orm[u'api.provider'], null=False)),
            ('diagnosis', models.ForeignKey(orm[u'api.diagnosis'], null=False))
        ))
        db.create_unique(m2m_table_name, ['provider_id', 'diagnosis_id'])


    def backwards(self, orm):
        # Adding M2M table for field diagnosis on 'Provider'
        m2m_table_name = db.shorten_name(u'api_provider_diagnosis')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('provider', models.ForeignKey(orm[u'api.provider'], null=False)),
            ('diagnosis', models.ForeignKey(orm[u'api.diagnosis'], null=False))
        ))
        db.create_unique(m2m_table_name, ['provider_id', 'diagnosis_id'])

        # Removing M2M table for field diagnoses on 'Provider'
        db.delete_table(db.shorten_name(u'api_provider_diagnoses'))


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
            'version_number': ('django.db.models.fields.PositiveIntegerField', [], {})
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
            'diagnoses': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['api.Diagnosis']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['api']