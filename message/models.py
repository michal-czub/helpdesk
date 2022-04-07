from django.utils import timezone
from django.db import models

class Message(models.Model):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"

    STATUS = [
        (NEW, "New"),
        (IN_PROGRESS, "In progress"),
        (RESOLVED, "Event resolved"),
    ]

    status = models.CharField(choices=STATUS, max_length=255)
    info = models.CharField(max_length=1000)
    status_changed_by = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
