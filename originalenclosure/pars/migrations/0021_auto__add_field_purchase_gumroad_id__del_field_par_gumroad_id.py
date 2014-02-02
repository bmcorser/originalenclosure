# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Purchase.gumroad_id'
        db.add_column('pars_purchase', 'gumroad_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=512, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Par.gumroad_id'
        db.delete_column('pars_par', 'gumroad_id')


    def backwards(self, orm):
        # Deleting field 'Purchase.gumroad_id'
        db.delete_column('pars_purchase', 'gumroad_id')

        # Adding field 'Par.gumroad_id'
        db.add_column('pars_par', 'gumroad_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=512, null=True, blank=True),
                      keep_default=False)


    models = {
        'pars.image': {
            'Meta': {'object_name': 'Image'},
            'dead': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '10000', 'blank': 'True'}),
            'seen': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 2, 2, 0, 0)', 'null': 'True'}),
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
            'result': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'run': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parsees'", 'to': "orm['pars.ParSeeRun']"})
        },
        'pars.parseerun': {
            'Meta': {'object_name': 'ParSeeRun'},
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        'pars.purchase': {
            'Meta': {'object_name': 'Purchase'},
            'gumroad_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'par': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pars.Par']"}),
            'pdf': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'sale': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'da9a951802974660944c030fedb561ed'", 'max_length': '32', 'primary_key': 'True'})
        }
    }

    complete_apps = ['pars']