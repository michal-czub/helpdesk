from django.db import models
from event.models import Event
import uuid

class Consultation(models.Model):
    event = models.ForeignKey(Event, related_name="consultations", on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    date = models.DateTimeField()
    is_confirmed = models.BooleanField(default=False)
