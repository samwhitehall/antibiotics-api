# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Provider'
        db.create_table(u'api_provider', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'api', ['Provider'])

        # Adding model 'Category'
        db.create_table(u'api_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'api', ['Category'])

        # Adding model 'Diagnosis'
        db.create_table(u'api_diagnosis', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Category'], null=True)),
        ))
        db.send_create_signal(u'api', ['Diagnosis'])

        # Adding model 'DecisionTree'
        db.create_table(u'api_decisiontree', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, unique=True, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Provider'], null=True)),
            ('diagnosis', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Diagnosis'], null=True)),
            ('decision_structure', self.gf('jsonfield.fields.JSONField')(blank=True)),
        ))
        db.send_create_signal(u'api', ['DecisionTree'])

        # Adding model 'Question'
        db.create_table(u'api_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('qid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('information', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'api', ['Question'])

        # Adding M2M table for field answers on 'Question'
        m2m_table_name = db.shorten_name(u'api_question_answers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm[u'api.question'], null=False)),
            ('questionchoice', models.ForeignKey(orm[u'api.questionchoice'], null=False))
        ))
        db.create_unique(m2m_table_name, ['question_id', 'questionchoice_id'])

        # Adding model 'QuestionChoice'
        db.create_table(u'api_questionchoice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'api', ['QuestionChoice'])

        # Adding model 'Treatment'
        db.create_table(u'api_treatment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('details', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'api', ['Treatment'])


    def backwards(self, orm):
        # Deleting model 'Provider'
        db.delete_table(u'api_provider')

        # Deleting model 'Category'
        db.delete_table(u'api_category')

        # Deleting model 'Diagnosis'
        db.delete_table(u'api_diagnosis')

        # Deleting model 'DecisionTree'
        db.delete_table(u'api_decisiontree')

        # Deleting model 'Question'
        db.delete_table(u'api_question')

        # Removing M2M table for field answers on 'Question'
        db.delete_table(db.shorten_name(u'api_question_answers'))

        # Deleting model 'QuestionChoice'
        db.delete_table(u'api_questionchoice')

        # Deleting model 'Treatment'
        db.delete_table(u'api_treatment')


    models = {
        u'api.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'api.decisiontree': {
            'Meta': {'object_name': 'DecisionTree'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'unique': 'True', 'blank': 'True'}),
            'decision_structure': ('jsonfield.fields.JSONField', [], {'blank': 'True'}),
            'diagnosis': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.Diagnosis']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.Provider']", 'null': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'api.diagnosis': {
            'Meta': {'object_name': 'Diagnosis'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.Category']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'api.provider': {
            'Meta': {'object_name': 'Provider'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'api.question': {
            'Meta': {'object_name': 'Question'},
            'answers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['api.QuestionChoice']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'information': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'qid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'api.questionchoice': {
            'Meta': {'object_name': 'QuestionChoice'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'api.treatment': {
            'Meta': {'object_name': 'Treatment'},
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['api']