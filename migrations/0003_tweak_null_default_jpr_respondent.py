# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'JoinProjectRequest.respondent'
        db.alter_column('hackathon_joinprojectrequest', 'respondent_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hackathon.Person'], null=True))


    def backwards(self, orm):
        
        # Changing field 'JoinProjectRequest.respondent'
        db.alter_column('hackathon_joinprojectrequest', 'respondent_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hackathon.Person']))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'hackathon.joinprojectrequest': {
            'Meta': {'object_name': 'JoinProjectRequest'},
            'do_answer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'do_send': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'volunteer_requests'", 'to': "orm['hackathon.Project']"}),
            'queued_for': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'requests_waiting'", 'symmetrical': 'False', 'to': "orm['hackathon.Person']"}),
            'respondent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hackathon.Person']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'volunteer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects_volunteered'", 'to': "orm['hackathon.Person']"})
        },
        'hackathon.person': {
            'Meta': {'object_name': 'Person'},
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'roles_willing': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['hackathon.RoleChoice']", 'symmetrical': 'False', 'blank': 'True'}),
            'skills_summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'hackathon.project': {
            'Meta': {'object_name': 'Project'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'repo': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'hackathon.projectneed': {
            'Meta': {'object_name': 'ProjectNeed'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number_slots': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'needs'", 'to': "orm['hackathon.Project']"}),
            'role_needed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hackathon.RoleChoice']"})
        },
        'hackathon.projectstaff': {
            'Meta': {'unique_together': "(('team_leader', 'project'),)", 'object_name': 'ProjectStaff'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'to': "orm['hackathon.Person']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'staff'", 'to': "orm['hackathon.Project']"}),
            'team_leader': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'hackathon.rolechoice': {
            'Meta': {'ordering': "('name',)", 'object_name': 'RoleChoice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['hackathon']
