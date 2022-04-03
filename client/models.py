from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import uuid

class Client(models.Model):
    phone_number = PhoneNumberField(unique=True, null=False, blank=False)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    company = models.CharField(max_length=255, unique=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    key = models.CharField(max_length=32, unique=True)
    # zmienić null i blank # todo
    url = models.URLField(max_length=255, null=True, blank=True)
