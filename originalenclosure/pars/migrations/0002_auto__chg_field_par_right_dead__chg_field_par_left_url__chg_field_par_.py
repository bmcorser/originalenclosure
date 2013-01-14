# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Par.right_dead'
        db.alter_column('pars_par', 'right_dead', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'Par.left_url'
        db.alter_column('pars_par', 'left_url', self.gf('django.db.models.fields.URLField')(max_length=10000, null=True))

        # Changing field 'Par.left_seen'
        db.alter_column('pars_par', 'left_seen', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Par.right_seen'
        db.alter_column('pars_par', 'right_seen', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Par.left_image'
        db.alter_column('pars_par', 'left_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True))

        # Changing field 'Par.right_url'
        db.alter_column('pars_par', 'right_url', self.gf('django.db.models.fields.URLField')(max_length=10000, null=True))

        # Changing field 'Par.hidden'
        db.alter_column('pars_par', 'hidden', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'Par.left_dead'
        db.alter_column('pars_par', 'left_dead', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'Par.right_image'
        db.alter_column('pars_par', 'right_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True))

    def backwards(self, orm):

        # Changing field 'Par.right_dead'
        db.alter_column('pars_par', 'right_dead', self.gf('django.db.models.fields.BooleanField')())

        # User chose to not deal with backwards NULL issues for 'Par.left_url'
        raise RuntimeError("Cannot reverse this migration. 'Par.left_url' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Par.left_seen'
        raise RuntimeError("Cannot reverse this migration. 'Par.left_seen' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Par.right_seen'
        raise RuntimeError("Cannot reverse this migration. 'Par.right_seen' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Par.left_image'
        raise RuntimeError("Cannot reverse this migration. 'Par.left_image' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Par.right_url'
        raise RuntimeError("Cannot reverse this migration. 'Par.right_url' and its values cannot be restored.")

        # Changing field 'Par.hidden'
        db.alter_column('pars_par', 'hidden', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Par.left_dead'
        db.alter_column('pars_par', 'left_dead', self.gf('django.db.models.fields.BooleanField')())

        # User chose to not deal with backwards NULL issues for 'Par.right_image'
        raise RuntimeError("Cannot reverse this migration. 'Par.right_image' and its values cannot be restored.")

    models = {
        'pars.par': {
            'Meta': {'object_name': 'Par'},
            'hidden': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'left_dead': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'left_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'left_seen': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'left_url': ('django.db.models.fields.URLField', [], {'max_length': '10000', 'null': 'True'}),
            'right_dead': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'right_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'right_seen': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'right_url': ('django.db.models.fields.URLField', [], {'max_length': '10000', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['pars']