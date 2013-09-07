# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models


class Migration(DataMigration):
    AGENTS = (
      u"ΓΕΑ/Β3",
      u"ΕΑ",
      u"Μ.Υ.",
      u"ΔΚΤΗΣ",
      u"ΥΔΚΤΗΣ",
      u"ΑΣΦΑΛΕΙΑ",
      u"RECEPTION",
      u"ΓΕΕΘΑ",
      )

    STATUSES = (
      "PENDING",
      "CONFIRMED",
      "CANCELED",
      "CHECKEDOUT",
      "UNKNOWN",
      )

    RESERVATION_TYPES = (
      u"ΤΑΚΤΙΚΟΣ",
      u"ΠΑΡ/ΣΤΗΣ",
      u"ΟΣΣΕΑΥ",
      u"ΜΟΝΑΔΑ",
      u"ΣΧΟΛΕΙΑ",
      u"CLIMS",
      )

    def forwards(self, orm):
        # Deleting field 'Receipt.rtype'
        for r in orm.Reservation.objects.all():
            AGENT2ID = dict([(v, i) for (i, v) in enumerate(self.AGENTS)])
            STATUS2ID = dict([(v, i) for (i, v) in enumerate(self.STATUSES)])
            RESERVATION_TYPE2ID = dict([(v, i) for (i, v) in enumerate(self.RESERVATION_TYPES)])
            if r.agent:
              r.agent = AGENT2ID[r.agent]
            if r.status:
              r.status = STATUS2ID[r.status]
            if r.res_type:
              r.res_type = RESERVATION_TYPE2ID[r.res_type]
            r.save()

    def backwards(self, orm):
        # Adding field 'Receipt.rtype'
        for r in orm.Reservation.objects.all():
            ID2AGENT = dict([a for a in enumerate(self.AGENTS)])
            ID2STATUS = dict([a for a in enumerate(self.STATUSES)])
            ID2RES_TYPE = dict([a for a in enumerate(self.RESERVATION_TYPES)])
            if r.agent:
              r.agent = ID2AGENT[r.agent]
            if r.status:
              r.status = ID2STATUS[r.status]
            if r.res_type:
              r.res_type = ID2RES_TYPE[r.res_type]
            r.save()

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
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
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
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'euro': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'pending': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reservation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'receipts'", 'to': "orm['reception.Reservation']"})
        },
        'reception.relative': {
            'Meta': {'object_name': 'Relative', '_ormbases': ['reception.Person']},
            'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['reception.Person']", 'unique': 'True', 'primary_key': 'True'}),
            'related': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'relatives'", 'null': 'True', 'to': "orm['reception.Person']"}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        },
        'reception.reservation': {
            'Meta': {'object_name': 'Reservation'},
            'agent': ('django.db.models.fields.IntegerField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'appartment': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'reservations'", 'null': 'True', 'to': "orm['reception.Appartment']"}),
            'book_ref': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'check_in': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'check_out': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reservations'", 'to': "orm['reception.MilitaryPerson']"}),
            'persons': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'res_type': ('django.db.models.fields.IntegerField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
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
