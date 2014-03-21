# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Course'
        db.create_table(u'course_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'course', ['Course'])

        # Adding model 'CourseContent'
        db.create_table(u'course_coursecontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['course.Course'])),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['course.Lesson'])),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'course', ['CourseContent'])

        # Adding model 'Lesson'
        db.create_table(u'course_lesson', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'course', ['Lesson'])

        # Adding model 'LessonContent'
        db.create_table(u'course_lessoncontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['course.Lesson'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['course.Item'])),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'course', ['LessonContent'])

        # Adding model 'Item'
        db.create_table(u'course_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('polymorphic_ctype', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'polymorphic_course.item_set', null=True, to=orm['contenttypes.ContentType'])),
            ('item_type', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'course', ['Item'])

        # Adding model 'Resource'
        db.create_table(u'course_resource', (
            (u'item_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['course.Item'], unique=True, primary_key=True)),
            ('body', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'course', ['Resource'])

        # Adding M2M table for field related on 'Resource'
        m2m_table_name = db.shorten_name(u'course_resource_related')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resource', models.ForeignKey(orm[u'course.resource'], null=False)),
            ('item', models.ForeignKey(orm[u'course.item'], null=False))
        ))
        db.create_unique(m2m_table_name, ['resource_id', 'item_id'])

        # Adding model 'ExternalResource'
        db.create_table(u'course_externalresource', (
            (u'item_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['course.Item'], unique=True, primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=255)),
        ))
        db.send_create_signal(u'course', ['ExternalResource'])

        # Adding model 'Test'
        db.create_table(u'course_test', (
            (u'item_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['course.Item'], unique=True, primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'course', ['Test'])

        # Adding model 'TestContents'
        db.create_table(u'course_testcontents', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('test', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['course.Test'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['course.Question'])),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'course', ['TestContents'])

        # Adding model 'Question'
        db.create_table(u'course_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('polymorphic_ctype', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'polymorphic_course.question_set', null=True, to=orm['contenttypes.ContentType'])),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('positive_feedback', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('negative_feedback', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'course', ['Question'])

        # Adding model 'QuestionOption'
        db.create_table(u'course_questionoption', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('correct', self.gf('django.db.models.fields.BooleanField')()),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='options', to=orm['course.Question'])),
        ))
        db.send_create_signal(u'course', ['QuestionOption'])


    def backwards(self, orm):
        # Deleting model 'Course'
        db.delete_table(u'course_course')

        # Deleting model 'CourseContent'
        db.delete_table(u'course_coursecontent')

        # Deleting model 'Lesson'
        db.delete_table(u'course_lesson')

        # Deleting model 'LessonContent'
        db.delete_table(u'course_lessoncontent')

        # Deleting model 'Item'
        db.delete_table(u'course_item')

        # Deleting model 'Resource'
        db.delete_table(u'course_resource')

        # Removing M2M table for field related on 'Resource'
        db.delete_table(db.shorten_name(u'course_resource_related'))

        # Deleting model 'ExternalResource'
        db.delete_table(u'course_externalresource')

        # Deleting model 'Test'
        db.delete_table(u'course_test')

        # Deleting model 'TestContents'
        db.delete_table(u'course_testcontents')

        # Deleting model 'Question'
        db.delete_table(u'course_question')

        # Deleting model 'QuestionOption'
        db.delete_table(u'course_questionoption')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'course.course': {
            'Meta': {'object_name': 'Course'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lessons': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['course.Lesson']", 'through': u"orm['course.CourseContent']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'course.coursecontent': {
            'Meta': {'ordering': "['order']", 'object_name': 'CourseContent'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course.Lesson']"}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'course.externalresource': {
            'Meta': {'object_name': 'ExternalResource', '_ormbases': [u'course.Item']},
            u'item_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['course.Item']", 'unique': 'True', 'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        },
        u'course.item': {
            'Meta': {'object_name': 'Item'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'polymorphic_course.item_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'course.lesson': {
            'Meta': {'object_name': 'Lesson'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['course.Item']", 'through': u"orm['course.LessonContent']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'course.lessoncontent': {
            'Meta': {'ordering': "['order']", 'object_name': 'LessonContent'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course.Item']"}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course.Lesson']"}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'course.question': {
            'Meta': {'object_name': 'Question'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'negative_feedback': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'polymorphic_course.question_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'positive_feedback': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'course.questionoption': {
            'Meta': {'object_name': 'QuestionOption'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'correct': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'options'", 'to': u"orm['course.Question']"})
        },
        u'course.resource': {
            'Meta': {'object_name': 'Resource', '_ormbases': [u'course.Item']},
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'item_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['course.Item']", 'unique': 'True', 'primary_key': 'True'}),
            'related': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'resources'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['course.Item']"})
        },
        u'course.test': {
            'Meta': {'object_name': 'Test', '_ormbases': [u'course.Item']},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'item_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['course.Item']", 'unique': 'True', 'primary_key': 'True'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['course.Question']", 'through': u"orm['course.TestContents']", 'symmetrical': 'False'})
        },
        u'course.testcontents': {
            'Meta': {'ordering': "['order']", 'object_name': 'TestContents'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course.Question']"}),
            'test': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course.Test']"})
        }
    }

    complete_apps = ['course']