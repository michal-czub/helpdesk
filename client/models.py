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
    url_message = models.URLField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_name(self):
        return {
            "name": self.name,
        }

    def get_details(self):
        return {
            "id": self.id,
            "url_message": self.url_message,
            "name": self.name,
            "company": self.company,
            "phone_number": str(self.phone_number),
            "email": self.email,
        }

    def save(self, *args, **kwargs):
        self.url_message = "http://127.0.0.1:8000/message/"# + str(self.id)
        super().save(*args, **kwargs)
