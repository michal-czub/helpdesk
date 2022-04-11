import datetime
from django.test import TestCase
from helpdesk import settings
from consultation.models import Consultation
from client.models import Client

class ConsultationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        client = Client.objects.create(phone_number="+48609500500", email="test@mail.com", key=123,
                                       name="client", company="company")
        Consultation.objects.create(client=client, date=datetime.datetime.now())

    def test_consultation_model_is_configured(self):
        assert "consultation" in settings.INSTALLED_APPS

    def test_client_details_method(self):
        consultation = Consultation.objects.first()
        client = Client.objects.first()
        self.assertEqual(consultation.get_client_details()["name"], client.name)
        self.assertEqual(consultation.get_client_details()["phone_number"], client.phone_number)
        self.assertEqual(consultation.get_client_details()["email"], client.email)

    def test_get_details(self):
        consultation = Consultation.objects.first()
        self.assertEqual(consultation.get_details()["id"], consultation.id)
        self.assertEqual(consultation.get_details()["is_confirmed"], consultation.is_confirmed)
        self.assertEqual(consultation.get_details()["date"], consultation.date)
        self.assertEqual(consultation.get_details()["client"], consultation.client.get_details_for_consultation())
