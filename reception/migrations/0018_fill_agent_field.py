# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models


class Migration(DataMigration):

    def forwards(self, orm):
        # Adding field 'Reservation.agent'
        for r in orm.Reservation.objects.all():
          if r.res_type == u"ΤΑΚΤΙΚΟΣ":
            try:
              if r.owner.militaryperson.active:
                r.agent = u"ΓΕΑ/Β3"
              else:
                r.agent = u"ΕΑ"
            except:
              print "Owner %s is a Person with id %d" % (r.owner.info(), r.owner.id)

          r.save()


    def backwards(self, orm):
        # Deleting field 'Reservation.agent'
        pass


    models = {
        'reception.appartment': {
            'Meta': {'object_name': 'Appartment'},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'bunk': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'appartments'", 'null': 'True', 'blank': 'True', 'to': "orm['reception.Category']"}),
            'double': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'ranking': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'rooms': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'single': ('django.db.models.fields.IntegerField', [], {'default': '2'})
        },
        'reception.category': {
            'Meta': {'object_name': 'Category'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ranking': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'reception.contactinfo': {
            'Meta': {'object_name': 'ContactInfo'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'contacts'", 'null': 'True', 'to': "orm['reception.Person']"}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        },
        'reception.damage': {
            'Meta': {'object_name': 'Damage'},
            'appartment': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'damages'", 'null': 'True', 'to': "orm['reception.Appartment']"}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fixed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notified': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reception.Unit']", 'null': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'reception.militaryperson': {
            'Meta': {'object_name': 'MilitaryPerson', '_ormbases': ['reception.Person']},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['reception.Person']", 'unique': 'True', 'primary_key': 'True'}),
            'rank': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'military_persons'", 'null': 'True', 'to': "orm['reception.Rank']"}),
            'speciality': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'reception.period': {
            'Meta': {'object_name': 'Period'},
            'end': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {})
        },
        'reception.person': {
            'Meta': {'object_name': 'Person'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'reception.rank': {
            'Meta': {'object_name': 'Rank'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'rank': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'short': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'weapon': ('django.db.models.fields.CharField', [], {'default': "'\\xce\\xa0\\xce\\x91'", 'max_length': '5'})
        },
        'reception.receipt': {
            'Meta': {'object_name': 'Receipt'},
            'euro': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'reservation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'receipts'", 'to': "orm['reception.Reservation']"}),
            'rtype': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'reception.relative': {
            'Meta': {'object_name': 'Relative', '_ormbases': ['reception.Person']},
            'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['reception.Person']", 'unique': 'True', 'primary_key': 'True'}),
            'related': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'relatives'", 'null': 'True', 'to': "orm['reception.Person']"}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        },
        'reception.reservation': {
            'Meta': {'object_name': 'Reservation'},
            'agent': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'appartment': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'reservations'", 'null': 'True', 'to': "orm['reception.Appartment']"}),
            'book_ref': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'check_in': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'check_out': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reservations'", 'to': "orm['reception.Person']"}),
            'persons': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'res_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'reception.staff': {
            'Meta': {'object_name': 'Staff', '_ormbases': ['reception.MilitaryPerson']},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'militaryperson_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['reception.MilitaryPerson']", 'unique': 'True', 'primary_key': 'True'})
        },
        'reception.unit': {
            'Meta': {'object_name': 'Unit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'reception.vehicle': {
            'Meta': {'object_name': 'Vehicle'},
            'brand': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'vehicles'", 'null': 'True', 'to': "orm['reception.Person']"}),
            'plate': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        'reception.visitor': {
            'Meta': {'object_name': 'Visitor', '_ormbases': ['reception.MilitaryPerson']},
            'member': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'militaryperson_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['reception.MilitaryPerson']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['reception']
