from django.test import TestCase
from helpdesk import settings
from application.models import Application
from project.models import Project

class ApplicationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        project = Project.objects.create(name="project")
        Application.objects.create(name="app", project=project)

    def test_application_model_is_configured(self):
        assert "application" in settings.INSTALLED_APPS

    def test_str_method(self):
        app = Application.objects.first()
        self.assertEqual(app.__str__(), "app")

    def test_get_name_method(self):
        app = Application.objects.first()
        self.assertEqual(app.get_name(), "app")

    def test_get_details(self):
        app = Application.objects.first()
        self.assertEqual(app.get_details()["id"], app.id)
        self.assertEqual(app.get_details()["name"], "app")

    def test_get_project_details(self):
        app = Application.objects.first()
        self.assertEqual(app.get_project_details()["id"], app.project.id)
        self.assertEqual(app.get_project_details()["name"], app.project.name)
