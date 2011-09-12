# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'Ticket.created'
        db.add_column('core_ticket', 'created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True), keep_default=False)

        # Adding field 'Ticket.modified'
        db.add_column('core_ticket', 'modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True), keep_default=False)

        # Adding field 'News.created'
        db.add_column('core_news', 'created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True), keep_default=False)

        # Adding field 'News.modified'
        db.add_column('core_news', 'modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True), keep_default=False)

        # Adding field 'Version.created'
        db.add_column('core_version', 'created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True), keep_default=False)

        # Adding field 'Version.modified'
        db.add_column('core_version', 'modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True), keep_default=False)

        # Adding field 'Status.modified'
        db.add_column('core_status', 'modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True), keep_default=False)

        # Adding field 'Status.created'
        db.add_column('core_status', 'created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True), keep_default=False)

        # Adding field 'Project.modified'
        db.add_column('core_project', 'modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True), keep_default=False)

        # Adding field 'Project.created'
        db.add_column('core_project', 'created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Deleting field 'Ticket.created'
        db.delete_column('core_ticket', 'created')

        # Deleting field 'Ticket.modified'
        db.delete_column('core_ticket', 'modified')

        # Deleting field 'News.created'
        db.delete_column('core_news', 'created')

        # Deleting field 'News.modified'
        db.delete_column('core_news', 'modified')

        # Deleting field 'Version.created'
        db.delete_column('core_version', 'created')

        # Deleting field 'Version.modified'
        db.delete_column('core_version', 'modified')

        # Deleting field 'Status.modified'
        db.delete_column('core_status', 'modified')

        # Deleting field 'Status.created'
        db.delete_column('core_status', 'created')

        # Deleting field 'Project.modified'
        db.delete_column('core_project', 'modified')

        # Deleting field 'Project.created'
        db.delete_column('core_project', 'created')
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.membership': {
            'Meta': {'object_name': 'Membership'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Project']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Role']"})
        },
        'core.news': {
            'Meta': {'object_name': 'News'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Project']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'core.priority': {
            'Meta': {'object_name': 'Priority'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'value': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'core.project': {
            'Meta': {'object_name': 'Project'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'through': "orm['core.Membership']", 'symmetrical': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'core.role': {
            'Meta': {'object_name': 'Role'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'core.status': {
            'Meta': {'object_name': 'Status'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'core.ticket': {
            'Meta': {'object_name': 'Ticket'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_tickets'", 'to': "orm['auth.User']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'priority': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Priority']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Project']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Status']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Version']"}),
            'workers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'tickets'", 'blank': 'True', 'to': "orm['auth.User']"})
        },
        'core.version': {
            'Meta': {'object_name': 'Version'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Project']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {})
        }
    }
    
    complete_apps = ['core']
