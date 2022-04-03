from django.db import models
from board.models import Board
import uuid

class Stage(models.Model):
    board = models.ForeignKey(Board, related_name="stages", on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    name = models.CharField(max_length=255, unique=True)
    order = models.IntegerField()
