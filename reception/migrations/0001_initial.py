# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Rank'
        db.create_table('reception_rank', (
            ('weapon', self.gf('django.db.models.fields.CharField')(default='\xce\xa0\xce\x91', max_length=5)),
            ('short', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rank', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('level', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal('reception', ['Rank'])

        # Adding model 'Person'
        db.create_table('reception_person', (
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
        ))
        db.send_create_signal('reception', ['Person'])

        # Adding model 'Vehicle'
        db.create_table('reception_vehicle', (
            ('plate', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('brand', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='vehicles', null=True, to=orm['reception.Person'])),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('reception', ['Vehicle'])

        # Adding model 'ContactInfo'
        db.create_table('reception_contactinfo', (
            ('mobile', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='contacts', null=True, to=orm['reception.Person'])),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
        ))
        db.send_create_signal('reception', ['ContactInfo'])

        # Adding model 'Relative'
        db.create_table('reception_relative', (
            ('person_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['reception.Person'], unique=True, primary_key=True)),
            ('relationship', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('related', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='relatives', null=True, to=orm['reception.Person'])),
        ))
        db.send_create_signal('reception', ['Relative'])

        # Adding model 'MilitaryPerson'
        db.create_table('reception_militaryperson', (
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('person_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['reception.Person'], unique=True, primary_key=True)),
            ('speciality', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('rank', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='military_persons', null=True, to=orm['reception.Rank'])),
        ))
        db.send_create_signal('reception', ['MilitaryPerson'])

        # Adding model 'Visitor'
        db.create_table('reception_visitor', (
            ('member', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('militaryperson_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['reception.MilitaryPerson'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('reception', ['Visitor'])

        # Adding model 'Staff'
        db.create_table('reception_staff', (
            ('category', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('militaryperson_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['reception.MilitaryPerson'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('reception', ['Staff'])

        # Adding model 'Category'
        db.create_table('reception_category', (
            ('ranking', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal('reception', ['Category'])

        # Adding model 'Appartment'
        db.create_table('reception_appartment', (
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='appartments', null=True, blank=True, to=orm['reception.Category'])),
            ('ranking', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('no', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('double', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('bunk', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('area', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('single', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('rooms', self.gf('django.db.models.fields.IntegerField')(default=1, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('reception', ['Appartment'])

        # Adding model 'Unit'
        db.create_table('reception_unit', (
            ('internal', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('reception', ['Unit'])

        # Adding model 'Damage'
        db.create_table('reception_damage', (
            ('info', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('appartment', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='damages', null=True, to=orm['reception.Appartment'])),
            ('notified', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reception.Unit'], null=True, blank=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('fixed', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('reception', ['Damage'])

        # Adding model 'Reservation'
        db.create_table('reception_reservation', (
            ('status', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('res_type', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('check_in', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('appartment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reservations', to=orm['reception.Appartment'])),
            ('persons', self.gf('django.db.models.fields.IntegerField')(default=1, null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reservations', to=orm['reception.Visitor'])),
            ('check_out', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('reception', ['Reservation'])

        # Adding model 'Period'
        db.create_table('reception_period', (
            ('start', self.gf('django.db.models.fields.DateField')()),
            ('end', self.gf('django.db.models.fields.DateField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('reception', ['Period'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Rank'
        db.delete_table('reception_rank')

        # Deleting model 'Person'
        db.delete_table('reception_person')

        # Deleting model 'Vehicle'
        db.delete_table('reception_vehicle')

        # Deleting model 'ContactInfo'
        db.delete_table('reception_contactinfo')

        # Deleting model 'Relative'
        db.delete_table('reception_relative')

        # Deleting model 'MilitaryPerson'
        db.delete_table('reception_militaryperson')

        # Deleting model 'Visitor'
        db.delete_table('reception_visitor')

        # Deleting model 'Staff'
        db.delete_table('reception_staff')

        # Deleting model 'Category'
        db.delete_table('reception_category')

        # Deleting model 'Appartment'
        db.delete_table('reception_appartment')

        # Deleting model 'Unit'
        db.delete_table('reception_unit')

        # Deleting model 'Damage'
        db.delete_table('reception_damage')

        # Deleting model 'Reservation'
        db.delete_table('reception_reservation')

        # Deleting model 'Period'
        db.delete_table('reception_period')
    
    
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
            'fixed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notified': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reception.Unit']", 'null': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'reception.militaryperson': {
            'Meta': {'object_name': 'MilitaryPerson', '_ormbases': ['reception.Person']},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['reception.Person']", 'unique': 'True', 'primary_key': 'True'}),
            'rank': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'military_persons'", 'null': 'True', 'to': "orm['reception.Rank']"}),
            'speciality': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'reception.period': {
            'Meta': {'object_name': 'Period'},
            'end': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
        'reception.relative': {
            'Meta': {'object_name': 'Relative', '_ormbases': ['reception.Person']},
            'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['reception.Person']", 'unique': 'True', 'primary_key': 'True'}),
            'related': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'relatives'", 'null': 'True', 'to': "orm['reception.Person']"}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        },
        'reception.reservation': {
            'Meta': {'object_name': 'Reservation'},
            'appartment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reservations'", 'to': "orm['reception.Appartment']"}),
            'check_in': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'check_out': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reservations'", 'to': "orm['reception.Visitor']"}),
            'persons': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'res_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'reception.staff': {
            'Meta': {'object_name': 'Staff', '_ormbases': ['reception.MilitaryPerson']},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
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
            'member': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'militaryperson_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['reception.MilitaryPerson']", 'unique': 'True', 'primary_key': 'True'})
        }
    }
    
    complete_apps = ['reception']
