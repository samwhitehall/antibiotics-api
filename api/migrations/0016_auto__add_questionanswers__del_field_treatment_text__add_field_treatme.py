# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'QuestionAnswers'
        db.create_table(u'api_questionanswers', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'api', ['QuestionAnswers'])

        # Deleting field 'Treatment.text'
        db.delete_column(u'api_treatment', 'text')

        # Adding field 'Treatment.details'
        db.add_column(u'api_treatment', 'details',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Deleting field 'Question.text'
        db.delete_column(u'api_question', 'text')

        # Adding field 'Question.label'
        db.add_column(u'api_question', 'label',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'Question.information'
        db.add_column(u'api_question', 'information',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding M2M table for field answers on 'Question'
        m2m_table_name = db.shorten_name(u'api_question_answers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm[u'api.question'], null=False)),
            ('questionanswers', models.ForeignKey(orm[u'api.questionanswers'], null=False))
        ))
        db.create_unique(m2m_table_name, ['question_id', 'questionanswers_id'])


    def backwards(self, orm):
        # Deleting model 'QuestionAnswers'
        db.delete_table(u'api_questionanswers')

        # Adding field 'Treatment.text'
        db.add_column(u'api_treatment', 'text',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Deleting field 'Treatment.details'
        db.delete_column(u'api_treatment', 'details')

        # Adding field 'Question.text'
        db.add_column(u'api_question', 'text',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Deleting field 'Question.label'
        db.delete_column(u'api_question', 'label')

        # Deleting field 'Question.information'
        db.delete_column(u'api_question', 'information')

        # Removing M2M table for field answers on 'Question'
        db.delete_table(db.shorten_name(u'api_question_answers'))


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
            'answers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['api.QuestionAnswers']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'information': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'qid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'api.questionanswers': {
            'Meta': {'object_name': 'QuestionAnswers'},
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