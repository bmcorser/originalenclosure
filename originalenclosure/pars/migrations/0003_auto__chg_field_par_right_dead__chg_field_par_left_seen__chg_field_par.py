# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Par.right_dead'
        db.alter_column('pars_par', 'right_dead', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Par.left_seen'
        db.alter_column('pars_par', 'left_seen', self.gf('django.db.models.fields.DateField')())

        # Changing field 'Par.right_seen'
        db.alter_column('pars_par', 'right_seen', self.gf('django.db.models.fields.DateField')())

        # Changing field 'Par.hidden'
        db.alter_column('pars_par', 'hidden', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Par.left_dead'
        db.alter_column('pars_par', 'left_dead', self.gf('django.db.models.fields.BooleanField')())

    def backwards(self, orm):

        # Changing field 'Par.right_dead'
        db.alter_column('pars_par', 'right_dead', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'Par.left_seen'
        db.alter_column('pars_par', 'left_seen', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Par.right_seen'
        db.alter_column('pars_par', 'right_seen', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Par.hidden'
        db.alter_column('pars_par', 'hidden', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'Par.left_dead'
        db.alter_column('pars_par', 'left_dead', self.gf('django.db.models.fields.NullBooleanField')(null=True))

    models = {
        'pars.par': {
            'Meta': {'object_name': 'Par'},
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'left_dead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'left_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'left_seen': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 13, 0, 0)'}),
            'left_url': ('django.db.models.fields.URLField', [], {'max_length': '10000', 'null': 'True'}),
            'right_dead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'right_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'right_seen': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 13, 0, 0)'}),
            'right_url': ('django.db.models.fields.URLField', [], {'max_length': '10000', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['pars']