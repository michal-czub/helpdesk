from django.db import models
import uuid

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def get_details(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    class Meta:
        ordering = ["name"]
