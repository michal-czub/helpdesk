from django.db import models
from staff.models import Staff
import uuid

class Team(models.Model):
    members = models.ManyToManyField(Staff, related_name="teams")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    name = models.CharField(max_length=500, unique=True)