from django.db import models
from staff.models import Staff
import uuid

class Team(models.Model):
    members = models.ManyToManyField(Staff, related_name="teams")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name

    def get_details(self):
        return {
            "id": self.id,
            "name": self.name
        }

    class Meta:
        ordering = ["id"]
