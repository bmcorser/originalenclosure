# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Purchase'
        db.create_table('pars_purchase', (
            ('uuid', self.gf('django.db.models.fields.CharField')(default='734f1927dcec41b2b12ca1e4ddcc9a18', max_length=32, primary_key=True)),
            ('par', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pars.Par'])),
            ('sale', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('pdf', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True)),
            ('gumroad_id', self.gf('django.db.models.fields.CharField')(default='', max_length=512, null=True, blank=True)),
        ))
        db.send_create_signal('pars', ['Purchase'])

        # Deleting field 'ParSee.result_bits'
        db.delete_column('pars_parsee', 'result_bits')

        # Adding field 'ParSee.result'
        db.add_column('pars_parsee', 'result',
                      self.gf('django.db.models.fields.BigIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Purchase'
        db.delete_table('pars_purchase')

        # Adding field 'ParSee.result_bits'
        db.add_column('pars_parsee', 'result_bits',
                      self.gf('django.db.models.fields.BigIntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'ParSee.result'
        db.delete_column('pars_parsee', 'result')


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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'c9d6320e79734f628c635c97387b9752'", 'max_length': '32', 'primary_key': 'True'})
        }
    }

    complete_apps = ['pars']