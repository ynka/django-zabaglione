from django.test import TestCase
from core.models import Project

class ObjectPermissionsTest(TestCase):
    fixtures = ['projects-users-objpermissions.json']

    def test_costam(self):
        project = Project.objects.all()[0]
        self.failUnlessEqual(project.name, 123)


