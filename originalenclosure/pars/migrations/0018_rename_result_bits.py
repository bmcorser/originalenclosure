# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_column('pars_parsee', 'result_bits', 'result')

    def backwards(self, orm):
        db.rename_column('pars_parsee', 'result', 'result_bits')

    models = {
        'pars.image': {
            'Meta': {'object_name': 'Image'},
            'dead': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '10000', 'blank': 'True'}),
            'seen': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 10, 10, 0, 0)', 'null': 'True'}),
            'source': ('django.db.models.fields.URLField', [], {'max_length': '10000', 'null': 'True', 'blank': 'True'})
        },
        'pars.par': {
            'Meta': {'ordering': "['number', 'created']", 'object_name': 'Par'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_buffer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'left': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'left'", 'unique': 'True', 'null': 'True', 'to': "orm['pars.Image']"}),
            'number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4'}),
            'right': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'right'", 'unique': 'True', 'null': 'True', 'to': "orm['pars.Image']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '204', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'pars.parsee': {
            'Meta': {'object_name': 'ParSee'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'par': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parsees'", 'to': "orm['pars.Par']"}),
            'result_bits': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'run': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parsees'", 'to': "orm['pars.ParSeeRun']"})
        },
        'pars.parseerun': {
            'Meta': {'object_name': 'ParSeeRun'},
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['pars']
