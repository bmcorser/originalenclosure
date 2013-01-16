# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Image'
        db.create_table('pars_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=10000, blank=True)),
            ('source', self.gf('django.db.models.fields.URLField')(max_length=10000)),
            ('seen', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 15, 0, 0), null=True)),
            ('dead', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('pars', ['Image'])

        # Adding field 'Par.left'
        db.add_column('pars_par', 'left',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='left', null=True, to=orm['pars.Image']),
                      keep_default=False)

        # Adding field 'Par.right'
        db.add_column('pars_par', 'right',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='right', null=True, to=orm['pars.Image']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Image'
        db.delete_table('pars_image')

        # Deleting field 'Par.left'
        db.delete_column('pars_par', 'left_id')

        # Deleting field 'Par.right'
        db.delete_column('pars_par', 'right_id')


    models = {
        'pars.image': {
            'Meta': {'object_name': 'Image'},
            'dead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '10000', 'blank': 'True'}),
            'seen': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 15, 0, 0)', 'null': 'True'}),
            'source': ('django.db.models.fields.URLField', [], {'max_length': '10000'})
        },
        'pars.par': {
            'Meta': {'ordering': "['number', 'created']", 'object_name': 'Par'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 15, 0, 0)'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'left': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'left'", 'null': 'True', 'to': "orm['pars.Image']"}),
            'left_dead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'left_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '10000', 'blank': 'True'}),
            'left_seen': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 15, 0, 0)', 'null': 'True'}),
            'left_source': ('django.db.models.fields.URLField', [], {'max_length': '10000'}),
            'number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4'}),
            'right': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'right'", 'null': 'True', 'to': "orm['pars.Image']"}),
            'right_dead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'right_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '10000', 'blank': 'True'}),
            'right_seen': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 15, 0, 0)', 'null': 'True'}),
            'right_source': ('django.db.models.fields.URLField', [], {'max_length': '10000'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['pars']