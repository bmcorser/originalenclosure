# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Par.created'
        db.add_column('pars_par', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 14, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Par.created'
        db.delete_column('pars_par', 'created')


    models = {
        'pars.par': {
            'Meta': {'object_name': 'Par'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 14, 0, 0)'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'left_dead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'left_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'left_seen': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 14, 0, 0)', 'null': 'True'}),
            'left_source': ('django.db.models.fields.URLField', [], {'max_length': '10000'}),
            'number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4'}),
            'right_dead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'right_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'right_seen': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 14, 0, 0)', 'null': 'True'}),
            'right_source': ('django.db.models.fields.URLField', [], {'max_length': '10000'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['pars']