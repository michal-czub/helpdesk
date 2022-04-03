from django.db import models
from project.models import Project
import uuid

class Application(models.Model):
    project = models.ForeignKey(Project, related_name="applications", on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    name = models.CharField(max_length=255, unique=True)
