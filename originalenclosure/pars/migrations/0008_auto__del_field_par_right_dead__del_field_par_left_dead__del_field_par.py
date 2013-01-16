# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Par.right_dead'
        db.delete_column('pars_par', 'right_dead')

        # Deleting field 'Par.left_dead'
        db.delete_column('pars_par', 'left_dead')

        # Deleting field 'Par.left_seen'
        db.delete_column('pars_par', 'left_seen')

        # Deleting field 'Par.right_seen'
        db.delete_column('pars_par', 'right_seen')

        # Deleting field 'Par.left_image'
        db.delete_column('pars_par', 'left_image')

        # Deleting field 'Par.left_source'
        db.delete_column('pars_par', 'left_source')

        # Deleting field 'Par.right_image'
        db.delete_column('pars_par', 'right_image')

        # Deleting field 'Par.right_source'
        db.delete_column('pars_par', 'right_source')


    def backwards(self, orm):
        # Adding field 'Par.right_dead'
        db.add_column('pars_par', 'right_dead',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Par.left_dead'
        db.add_column('pars_par', 'left_dead',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Par.left_seen'
        db.add_column('pars_par', 'left_seen',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 15, 0, 0), null=True),
                      keep_default=False)

        # Adding field 'Par.right_seen'
        db.add_column('pars_par', 'right_seen',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 15, 0, 0), null=True),
                      keep_default=False)

        # Adding field 'Par.left_image'
        db.add_column('pars_par', 'left_image',
                      self.gf('django.db.models.fields.files.ImageField')(default='', max_length=10000, blank=True),
                      keep_default=False)

        # Adding field 'Par.left_source'
        db.add_column('pars_par', 'left_source',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=10000),
                      keep_default=False)

        # Adding field 'Par.right_image'
        db.add_column('pars_par', 'right_image',
                      self.gf('django.db.models.fields.files.ImageField')(default='', max_length=10000, blank=True),
                      keep_default=False)

        # Adding field 'Par.right_source'
        db.add_column('pars_par', 'right_source',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=10000),
                      keep_default=False)


    models = {
        'pars.image': {
            'Meta': {'object_name': 'Image'},
            'dead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '10000', 'blank': 'True'}),
            'seen': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 16, 0, 0)', 'null': 'True'}),
            'source': ('django.db.models.fields.URLField', [], {'max_length': '10000'})
        },
        'pars.par': {
            'Meta': {'ordering': "['number', 'created']", 'object_name': 'Par'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 16, 0, 0)'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'left': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'left'", 'null': 'True', 'to': "orm['pars.Image']"}),
            'number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4'}),
            'right': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'right'", 'null': 'True', 'to': "orm['pars.Image']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['pars']