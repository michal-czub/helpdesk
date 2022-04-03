from django.db import models
from project.models import Project
import uuid

class Board(models.Model):
    project = models.ForeignKey(Project, related_name="boards", on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def get_details(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def get_project_details(self):
        return self.project.get_details()