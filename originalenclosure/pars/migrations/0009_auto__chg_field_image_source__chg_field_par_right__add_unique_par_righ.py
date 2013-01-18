# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Image.source'
        db.alter_column('pars_image', 'source', self.gf('django.db.models.fields.URLField')(max_length=10000, null=True))

        # Changing field 'Par.right'
        db.alter_column('pars_par', 'right_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, null=True, to=orm['pars.Image']))
        # Adding unique constraint on 'Par', fields ['right']
        db.create_unique('pars_par', ['right_id'])


        # Changing field 'Par.left'
        db.alter_column('pars_par', 'left_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, null=True, to=orm['pars.Image']))
        # Adding unique constraint on 'Par', fields ['left']
        db.create_unique('pars_par', ['left_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Par', fields ['left']
        db.delete_unique('pars_par', ['left_id'])

        # Removing unique constraint on 'Par', fields ['right']
        db.delete_unique('pars_par', ['right_id'])


        # Changing field 'Image.source'
        db.alter_column('pars_image', 'source', self.gf('django.db.models.fields.URLField')(default='', max_length=10000))

        # Changing field 'Par.right'
        db.alter_column('pars_par', 'right_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['pars.Image']))

        # Changing field 'Par.left'
        db.alter_column('pars_par', 'left_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['pars.Image']))

    models = {
        'pars.image': {
            'Meta': {'object_name': 'Image'},
            'dead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '10000', 'blank': 'True'}),
            'seen': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 18, 0, 0)', 'null': 'True'}),
            'source': ('django.db.models.fields.URLField', [], {'max_length': '10000', 'null': 'True', 'blank': 'True'})
        },
        'pars.par': {
            'Meta': {'ordering': "['number', 'created']", 'object_name': 'Par'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 18, 0, 0)'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'left': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'left'", 'unique': 'True', 'null': 'True', 'to': "orm['pars.Image']"}),
            'number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4'}),
            'right': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'right'", 'unique': 'True', 'null': 'True', 'to': "orm['pars.Image']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['pars']