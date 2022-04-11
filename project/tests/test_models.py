from django.test import TestCase
from helpdesk import settings
from project.models import Project

class ProjectModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Project.objects.create(name="test_project")

    def test_project_model_is_configured(self):
        assert "project" in settings.INSTALLED_APPS

    def test_str_method(self):
        self.assertEqual(Project.objects.first().__str__(), "test_project")

    def test_get_details_method(self):
        project = Project.objects.first()
        self.assertEqual(project.get_details()["name"], "test_project")
        self.assertEqual(project.get_details()["id"], project.id)
