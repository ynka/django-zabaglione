from django.contrib.contenttypes.generic import GenericTabularInline

from object_permissions.models import ObjectPermission

class ObjectPermissionInline(GenericTabularInline):
    model = ObjectPermission
    raw_id_fields = ['user']
    extra = 1
