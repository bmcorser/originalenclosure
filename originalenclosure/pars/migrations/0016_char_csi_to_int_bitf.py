# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

def csints_to_bitsint(pks_values):
    return_list = []
    for pk, value in pks_values:
        return_list.append((pk, int(''.join(value.split(',')), 2)))
    return return_list

def bitsint_to_csints(pks_values):
    return_list = []
    for pk, value in pks_values:
        cs_ints = ','.join((list('{0:02}'.format(int(bin(value)[2:])))))
        return_list.append((pk, cs_ints))
    return return_list

class Migration(DataMigration):

    def forwards(self, orm):
        pks_values = orm['pars.ParSee'].objects.all().values_list('id', 'result')
        bitfield_pks_values = csints_to_bitsint(pks_values)
        for pk, value in bitfield_pks_values:
            db.execute("""
            UPDATE pars_parsee SET result_bits = {1} WHERE id = {0};
            """.format(pk, value))

    def backwards(self, orm):
        pks_values = orm['pars.ParSee'].objects.all().values_list('id', 'result_bits')
        csints_pks_values = bitsint_to_csints(pks_values)
        for pk, value in csints_pks_values:
            db.execute("""
            UPDATE pars_parsee SET result = {1} WHERE id = {0};
            """.format(pk, value))

    models = {
        'pars.image': {
            'Meta': {'object_name': 'Image'},
            'dead': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '10000', 'blank': 'True'}),
            'seen': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 10, 10, 0, 0)', 'null': 'True'}),
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
            'result': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '3'}),
            'result_bits': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'run': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parsees'", 'to': "orm['pars.ParSeeRun']"})
        },
        'pars.parseerun': {
            'Meta': {'object_name': 'ParSeeRun'},
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['pars']
    symmetrical = True
