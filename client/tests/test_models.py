from django.test import TestCase
from helpdesk import settings
from client.models import Client

class ClientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Client.objects.create(phone_number="+48609500500", email="test@mail.com", key=123,
                                       name="client", company="company")

    def test_client_model_is_configured(self):
        assert "client" in settings.INSTALLED_APPS

    def test_str_method(self):
        client = Client.objects.first()
        self.assertEqual(client.__str__(), "client")

    def test_get_name_method(self):
        client = Client.objects.first()
        self.assertEqual(client.get_name(), "client")

    def test_get_details_method(self):
        client = Client.objects.first()
        self.assertEqual(client.get_details()["name"], client.name)
        self.assertEqual(client.get_details()["phone_number"], client.phone_number)
        self.assertEqual(client.get_details()["email"], client.email)
        self.assertEqual(client.get_details()["id"], client.id)
        self.assertEqual(client.get_details()["company"], client.company)
        self.assertEqual(client.get_details()["url_message"], client.url_message)
