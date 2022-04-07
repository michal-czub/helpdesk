from django.db import models
from event.models import Event
from client.models import Client
import uuid

class Consultation(models.Model):
    event = models.ForeignKey(Event, related_name="consultations", on_delete=models.CASCADE,
                              blank=True, null=True)
    client = models.ForeignKey(Client, related_name="consultations", on_delete=models.CASCADE,
                               blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    date = models.DateTimeField()
    is_confirmed = models.BooleanField(default=False)

    def get_client_details(self):
        return self.client.get_details_for_consultation()

    def get_details(self):
        return {
            "id": self.id,
            "is_confirmed": self.is_confirmed,
            "date": self.date,
            "client": self.get_client_details(),
        }
