# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Par'
        db.create_table('pars_par', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('left_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('left_url', self.gf('django.db.models.fields.URLField')(max_length=10000)),
            ('left_seen', self.gf('django.db.models.fields.DateField')()),
            ('left_dead', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('right_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('right_url', self.gf('django.db.models.fields.URLField')(max_length=10000)),
            ('right_seen', self.gf('django.db.models.fields.DateField')()),
            ('right_dead', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('pars', ['Par'])


    def backwards(self, orm):
        # Deleting model 'Par'
        db.delete_table('pars_par')


    models = {
        'pars.par': {
            'Meta': {'object_name': 'Par'},
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'left_dead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'left_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'left_seen': ('django.db.models.fields.DateField', [], {}),
            'left_url': ('django.db.models.fields.URLField', [], {'max_length': '10000'}),
            'right_dead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'right_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'right_seen': ('django.db.models.fields.DateField', [], {}),
            'right_url': ('django.db.models.fields.URLField', [], {'max_length': '10000'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['pars']