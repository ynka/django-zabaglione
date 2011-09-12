from django.test import TestCase
from core.models import Project

class ObjectPermissionsTest(TestCase):
    fixtures = ['projects-users-objpermissions.json']

    def test_user_has_permissions(self):
        project = Project.objects.all()[0]
        self.assertTrue(project.name is not None)


