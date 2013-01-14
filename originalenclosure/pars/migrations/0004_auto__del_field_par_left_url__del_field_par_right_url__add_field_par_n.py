# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Par.left_url'
        db.delete_column('pars_par', 'left_url')

        # Deleting field 'Par.right_url'
        db.delete_column('pars_par', 'right_url')

        # Adding field 'Par.number'
        db.add_column('pars_par', 'number',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=4),
                      keep_default=False)

        # Adding field 'Par.left_source'
        db.add_column('pars_par', 'left_source',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=10000, blank=True),
                      keep_default=False)

        # Adding field 'Par.right_source'
        db.add_column('pars_par', 'right_source',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=10000, blank=True),
                      keep_default=False)


        # Changing field 'Par.left_seen'
        db.alter_column('pars_par', 'left_seen', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Par.right_seen'
        db.alter_column('pars_par', 'right_seen', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Par.left_image'
        db.alter_column('pars_par', 'left_image', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100))

        # Changing field 'Par.right_image'
        db.alter_column('pars_par', 'right_image', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100))

    def backwards(self, orm):
        # Adding field 'Par.left_url'
        db.add_column('pars_par', 'left_url',
                      self.gf('django.db.models.fields.URLField')(max_length=10000, null=True),
                      keep_default=False)

        # Adding field 'Par.right_url'
        db.add_column('pars_par', 'right_url',
                      self.gf('django.db.models.fields.URLField')(max_length=10000, null=True),
                      keep_default=False)

        # Deleting field 'Par.number'
        db.delete_column('pars_par', 'number')

        # Deleting field 'Par.left_source'
        db.delete_column('pars_par', 'left_source')

        # Deleting field 'Par.right_source'
        db.delete_column('pars_par', 'right_source')


        # Changing field 'Par.left_seen'
        db.alter_column('pars_par', 'left_seen', self.gf('django.db.models.fields.DateField')())

        # Changing field 'Par.right_seen'
        db.alter_column('pars_par', 'right_seen', self.gf('django.db.models.fields.DateField')())

        # Changing field 'Par.left_image'
        db.alter_column('pars_par', 'left_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True))

        # Changing field 'Par.right_image'
        db.alter_column('pars_par', 'right_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True))

    models = {
        'pars.par': {
            'Meta': {'object_name': 'Par'},
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'left_dead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'left_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'left_seen': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 13, 0, 0)', 'null': 'True'}),
            'left_source': ('django.db.models.fields.URLField', [], {'max_length': '10000', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4'}),
            'right_dead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'right_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'right_seen': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 13, 0, 0)', 'null': 'True'}),
            'right_source': ('django.db.models.fields.URLField', [], {'max_length': '10000', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['pars']