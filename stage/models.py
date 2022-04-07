from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from board.models import Board
import uuid

class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    # nadpisuje
    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    qs = qs.filter(**query)
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(OrderField, self).pre_save(model_instance, add)

class Stage(models.Model):
    board = models.ForeignKey(Board, related_name="stages", on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    name = models.CharField(max_length=255, unique=True)
    #order = models.IntegerField(null=True)
    order = OrderField(blank=True, for_fields=["board"])

    def __str__(self):
        return self.name

    def get_details(self):
        return {
            "id": self.id,
            "name": self.name,
            "order": self.order,
        }

    def get_name(self):
        return self.name

    class Meta:
        ordering = ["order"]
