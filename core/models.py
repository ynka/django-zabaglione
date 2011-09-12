from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
import django_filters
from django.core.urlresolvers import reverse
from object_permissions.models import ObjectPermission

from haystack import indexes
from haystack import site

class ProjectManager(models.Manager):
    def for_user(self, user):
        '''
        Zwraca queryset z wszystkimi projektami, do ktorych dany user ma
        uprawnienie can_view  (w przypadku superusera - po prostu
        wszystkie projecty)
        '''

        qs = self.get_query_set()
        if not user.is_superuser:
            # ograniczenie, gdy nie jest superuserem
            qs = self.get_query_set().filter(permissions__user=user,permissions__can_view=True)

        return qs

class Project(TimeStampedModel):
    name = models.CharField(max_length=50)
    description = models.TextField()
    repository_path = models.CharField(max_length=300, null=True, blank=True,
                                       help_text=_('Enter local, absolute Mercurial repository path'))

    # reverse generic relation - for convenience
    permissions = generic.GenericRelation(ObjectPermission)

    objects = ProjectManager()

    def __unicode__(self):
        return unicode(self.name)

    def get_absolute_url(self):
        return reverse('project_detail_url',kwargs={'object_id': self.pk})

class Version(TimeStampedModel):
    name = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    is_closed = models.BooleanField(default=False)
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return unicode(self.name)

class Status(TimeStampedModel):
    name = models.CharField(max_length=50)
    is_closed = models.BooleanField(default=False)


    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name_plural = 'statuses'

class Priority(models.Model):
    name = models.CharField(max_length=50)
    value = models.SmallIntegerField()

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name_plural = 'priorities'

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name_plural = 'categories'

class Ticket(TimeStampedModel):
    title = models.CharField(max_length=300)
    description = models.TextField()
    version = models.ForeignKey(Version,blank=True,null=True)
    status = models.ForeignKey(Status,blank=True,null=True)
    priority = models.ForeignKey(Priority,blank=True,null=True)
    project = models.ForeignKey(Project)
    author = models.ForeignKey(User, related_name="created_tickets")
    workers = models.ManyToManyField(User, related_name="tickets",blank=True)
    related = models.ManyToManyField("self",through="RelatedTickets",symmetrical=False,blank=True)
    category = models.ForeignKey(Category,blank=True,null=True)

    def __unicode__(self):
        return unicode(self.title)

    def get_absolute_url(self):
        return reverse('ticket_detail_url',kwargs={'project_id': self.project.pk, 'object_id': self.pk})

class RelatedTickets(models.Model):
    first = models.ForeignKey(Ticket,related_name="first_set")
    second = models.ForeignKey(Ticket,related_name="second_set")
    RELATION_CHOICES = (
            ('D',_('duplicates')),
            ('B',_('is blocked by')),
            ('R',_('is related to')),
            ) 
    relation = models.CharField(max_length=1,choices=RELATION_CHOICES)


class Role(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return unicode(self.name)

class News(TimeStampedModel):
    title = models.CharField(max_length=300)
    content = models.TextField()
    project = models.ForeignKey(Project)
    author = models.ForeignKey(User)

    class Meta:
        verbose_name_plural = 'news'

    def __unicode__(self):
        return unicode(self.title)

    def get_absolute_url(self):
        return reverse('news_detail_url', kwargs={'project_id' : self.project.pk, 'object_id' : self.pk})

class TicketIndex(indexes.SearchIndex):
    text = indexes.CharField(use_template=True,document=True)
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')

class ProjectIndex(indexes.SearchIndex):
    text = indexes.CharField(use_template=True,document=True)
    name = indexes.CharField(model_attr='name')
    description = indexes.CharField(model_attr="description")


class NewsIndex(indexes.SearchIndex):
    text = indexes.CharField(use_template=True,document=True)
    title = indexes.CharField(model_attr='title')
    content = indexes.CharField(model_attr='content')


site.register(Project,ProjectIndex)
site.register(Ticket, TicketIndex)
site.register(News,NewsIndex)
