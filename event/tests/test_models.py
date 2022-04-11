import datetime
from django.test import TestCase
from helpdesk import settings
from event.models import Event
from application.models import Application
from project.models import Project
from client.models import Client
from stage.models import Stage
from board.models import Board

class EventModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        project = Project.objects.create(name="project")
        app = Application.objects.create(name="app", project=project)
        client = Client.objects.create(phone_number="+48609500500", email="test@mail.com", key=123,
                              name="client", company="company")
        board = Board.objects.create(name="board", project=project)
        stage = Stage.objects.create(name="stage", order=0, board=board)
        Event.objects.create(signature="Z 14/5/2022/48", reported_at=datetime.datetime.now(),
                             status="Event resolved", subject="I need a new feature",
                             app=app, client=client, stage=stage)

    def test_event_model_is_configured(self):
        assert "event" in settings.INSTALLED_APPS

    def test_str_method(self):
        event = Event.objects.first()
        self.assertEqual(event.__str__(), "Z 14/5/2022/48")

    def test_get_client_name_method(self):
        event = Event.objects.first()
        self.assertEqual(event.get_client_name(), "client")

    def test_get_client_details_method(self):
        event = Event.objects.first()
        self.assertEqual(event.get_client_details()["name"], event.client.name)
        self.assertEqual(event.get_client_details()["phone_number"], event.client.phone_number)
        self.assertEqual(event.get_client_details()["email"], event.client.email)
        self.assertEqual(event.get_client_details()["id"], event.client.id)
        self.assertEqual(event.get_client_details()["company"], event.client.company)
        self.assertEqual(event.get_client_details()["url_message"], event.client.url_message)

    def test_get_stage_name_method(self):
        event = Event.objects.first()
        self.assertEqual(event.get_stage_name(), event.stage.name)

    def test_get_app_name_method(self):
        event = Event.objects.first()
        self.assertEqual(event.get_app_name(), event.app.name)

    def test_get_staff_name_method(self):
        event = Event.objects.first()
        self.assertEqual(event.get_staff_name(), None)

    def test_get_staff_details_method(self):
        event = Event.objects.first()
        self.assertEqual(event.get_staff_details(), None)

    def test_has_attachment_method(self):
        event = Event.objects.first()
        self.assertEqual(event.has_attachment(), False)

    def test_get_shortened_details_method(self):
        event = Event.objects.first()
        self.assertEqual(event.get_shortened_details()["id"], event.id)
        self.assertEqual(event.get_shortened_details()["signature"], event.signature)
        self.assertEqual(event.get_shortened_details()["created_at"], event.created_at)
        self.assertEqual(event.get_shortened_details()["client_name"], event.get_client_name())
        self.assertEqual(event.get_shortened_details()["app"], event.get_app_name())
        self.assertEqual(event.get_shortened_details()["subject"], event.subject)
        self.assertEqual(event.get_shortened_details()["functionality"], event.functionality)
        self.assertEqual(event.get_shortened_details()["staff"], event.get_staff_details())

    def test_get_all_details_method(self):
        event = Event.objects.first()
        data = event.get_all_details()
        self.assertEqual(data["id"], event.id)
        self.assertEqual(data["signature"], event.signature)
        self.assertEqual(data["created_at"], event.created_at)
        self.assertEqual(data["app"], event.get_app_name())
        self.assertEqual(data["subject"], event.subject)
        self.assertEqual(data["functionality"], event.functionality)
        self.assertEqual(data["staff"], event.get_staff_details())
        self.assertEqual(data["reported_at"], event.reported_at)
        self.assertEqual(data["finished_at"], event.finished_at)
        self.assertEqual(data["status"], event.status)
        self.assertEqual(data["priority"], event.priority)
        self.assertEqual(data["label"], event.label)
        self.assertEqual(data["description"], event.description)
        self.assertEqual(data["attachment"], event.attachment)
        self.assertEqual(data["is_assana_integrated"], event.is_assana_integrated)
        self.assertEqual(data["client"], event.client)
        self.assertEqual(data["board"], event.board)
