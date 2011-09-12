from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class ObjectPermission(models.Model):
    user = models.ForeignKey(User)
    can_view = models.BooleanField();
    can_change = models.BooleanField();
    can_delete = models.BooleanField();

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return u"User %s: permission for %s (id %d)" % (self.user.username, self.content_type.name, self.object_id)
