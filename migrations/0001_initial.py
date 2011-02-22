# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Person'
        db.create_table('hackathon_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=50, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('bio', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('skills_summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('hackathon', ['Person'])

        # Adding M2M table for field roles_willing on 'Person'
        db.create_table('hackathon_person_roles_willing', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm['hackathon.person'], null=False)),
            ('rolechoice', models.ForeignKey(orm['hackathon.rolechoice'], null=False))
        ))
        db.create_unique('hackathon_person_roles_willing', ['person_id', 'rolechoice_id'])

        # Adding model 'Project'
        db.create_table('hackathon_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=50, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('repo', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('hackathon', ['Project'])

        # Adding model 'ProjectNeed'
        db.create_table('hackathon_projectneed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='needs', to=orm['hackathon.Project'])),
            ('role_needed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hackathon.RoleChoice'])),
            ('number_slots', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal('hackathon', ['ProjectNeed'])

        # Adding model 'ProjectStaff'
        db.create_table('hackathon_projectstaff', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='staff', to=orm['hackathon.Project'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='projects', to=orm['hackathon.Person'])),
            ('team_leader', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('hackathon', ['ProjectStaff'])

        # Adding unique constraint on 'ProjectStaff', fields ['team_leader', 'project']
        db.create_unique('hackathon_projectstaff', ['team_leader', 'project_id'])

        # Adding M2M table for field roles on 'ProjectStaff'
        db.create_table('hackathon_projectstaff_roles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('projectstaff', models.ForeignKey(orm['hackathon.projectstaff'], null=False)),
            ('rolechoice', models.ForeignKey(orm['hackathon.rolechoice'], null=False))
        ))
        db.create_unique('hackathon_projectstaff_roles', ['projectstaff_id', 'rolechoice_id'])

        # Adding model 'RoleChoice'
        db.create_table('hackathon_rolechoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('hackathon', ['RoleChoice'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'ProjectStaff', fields ['team_leader', 'project']
        db.delete_unique('hackathon_projectstaff', ['team_leader', 'project_id'])

        # Deleting model 'Person'
        db.delete_table('hackathon_person')

        # Removing M2M table for field roles_willing on 'Person'
        db.delete_table('hackathon_person_roles_willing')

        # Deleting model 'Project'
        db.delete_table('hackathon_project')

        # Deleting model 'ProjectNeed'
        db.delete_table('hackathon_projectneed')

        # Deleting model 'ProjectStaff'
        db.delete_table('hackathon_projectstaff')

        # Removing M2M table for field roles on 'ProjectStaff'
        db.delete_table('hackathon_projectstaff_roles')

        # Deleting model 'RoleChoice'
        db.delete_table('hackathon_rolechoice')


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
            'roles': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['hackathon.RoleChoice']", 'symmetrical': 'False', 'blank': 'True'}),
            'team_leader': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'hackathon.rolechoice': {
            'Meta': {'ordering': "('name',)", 'object_name': 'RoleChoice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['hackathon']
