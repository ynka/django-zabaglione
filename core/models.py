from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.utils.translation import ugettext_lazy as _
from django.template.loader import get_template, render_to_string
from django.template import Context
from django_extensions.db.models import TimeStampedModel
from django.conf import settings
from object_permissions.models import ObjectPermission
import django_filters

class ProjectManager(models.Manager):
    def for_user(self, user):
        '''
        Returns queryset with projects that user can_view (in case of admin - all projects)
        '''
        qs = self.get_query_set()
        if not user.is_superuser:
            qs = self.get_query_set().filter(permissions__user=user,permissions__can_view=True)
        return qs

class Project(TimeStampedModel):
    name = models.CharField(max_length=50, verbose_name=_('name'))
    description = models.TextField(verbose_name=_('description'))
    repository_path = models.CharField(max_length=300, null=True, blank=True, verbose_name=_('repository path'), help_text=_('Enter local, absolute Mercurial repository path'))
    # reverse generic relation - for convenience
    permissions = generic.GenericRelation(ObjectPermission, verbose_name=_('permissions'))
    objects = ProjectManager()

    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _('projects')

    def __unicode__(self):
        return unicode(self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('project_detail_url', (), {'object_id': self.pk})

class Version(TimeStampedModel):
    name = models.CharField(max_length=50, verbose_name=_('name'))
    start_date = models.DateTimeField(verbose_name=_('start date'))
    due_date = models.DateTimeField(verbose_name=_('deadline'))
    is_closed = models.BooleanField(default=False, verbose_name=_('is closed?'))
    project = models.ForeignKey(Project)

    class Meta:
        verbose_name = _('version')
        verbose_name_plural = _('versions')

    def __unicode__(self):
        return unicode(self.name)

class Status(TimeStampedModel):
    name = models.CharField(max_length=50, verbose_name=_('name'))
    is_closed = models.BooleanField(default=False, verbose_name=_('is closed?'))

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = _('status')
        verbose_name_plural = _('statuses')

class Priority(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('name'))
    value = models.SmallIntegerField(verbose_name=_('value'))

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = _('priority')
        verbose_name_plural = _('priorities')

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('name'))

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __unicode__(self):
        return unicode(self.name)

class Ticket(TimeStampedModel):
    title = models.CharField(max_length=300, verbose_name=_('title'))
    description = models.TextField(verbose_name=_('description'))
    version = models.ForeignKey(Version,blank=True,null=True)
    status = models.ForeignKey(Status,blank=True,null=True)
    priority = models.ForeignKey(Priority,blank=True,null=True)
    project = models.ForeignKey(Project)
    author = models.ForeignKey(User, related_name="created_tickets")
    workers = models.ManyToManyField(User, related_name=_("tickets"),blank=True)
    related = models.ManyToManyField("self",through="RelatedTickets",symmetrical=False,blank=True)
    category = models.ForeignKey(Category,blank=True,null=True)
    observers = models.ManyToManyField(User, related_name=_('observed_tickets'), blank=True, null=True)

    class Meta:
        verbose_name = _('ticket')
        verbose_name_plural = _('tickets')

    def __unicode__(self):
        return unicode(self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('ticket_detail_url', (), {'project_id': self.project.pk, 'object_id': self.pk})

    def send_mails(self, action):
        current_site = Site.objects.get_current()
        url =  '%s%s' % (current_site, self.get_absolute_url())
        d = Context({'url':url, 'title':self.title, 'content':self.description})
        subject = render_to_string('core/ticket_%s_subject.txt' % action, {'title':self.title}).replace('\n', '')
        message = render_to_string('core/ticket_%s_message.html' % action, d)
        recipients = []
        recipients.append(self.author.email)
        recipients.extend([user.email for user in self.observers.all()])
        recipients.extend([user.email for user in self.workers.all()])
        recipients = list(set(recipients))
        from_email = settings.DEFAULT_FROM_EMAIL
        msg = EmailMessage(subject, message, from_email, recipients)
        msg.content_subtype = 'html'
        msg.send()


class RelatedTickets(models.Model):
    first = models.ForeignKey(Ticket,related_name=_("first_set"))
    second = models.ForeignKey(Ticket,related_name=_("second_set"))
    RELATION_CHOICES = (
            ('D',_('duplicates')),
            ('B',_('is blocked by')),
            ('R',_('is related to')),
            ) 
    relation = models.CharField(max_length=1,choices=RELATION_CHOICES)


class Role(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('name'))

    def __unicode__(self):
        return unicode(self.name)

class News(TimeStampedModel):
    title = models.CharField(max_length=300, verbose_name=_('title'))
    content = models.TextField(verbose_name=_('content'))
    project = models.ForeignKey(Project)
    author = models.ForeignKey(User)

    class Meta:
        verbose_name = _('news')
        verbose_name_plural = _('news')

    def __unicode__(self):
        return unicode(self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('news_detail_url', (),  {'project_id' : self.project.pk, 'object_id' : self.pk})

