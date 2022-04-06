from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from phonenumber_field.modelfields import PhoneNumberField
import uuid

class StaffManager(BaseUserManager):
    def create_user(self, phone_number, name, email, password=None, is_active=True, is_staff=True, is_admin=False):
        if not phone_number:
            raise ValueError("Staff member must have a phone number")
        if not password:
            raise ValueError("Staff member must have a password")
        user = self.model(
            phone_number=phone_number,
            name=name,
            email=email,
        )
        user.set_password(password)
        user.is_active = is_active
        user.is_staff = is_staff
        user.is_admin = is_admin
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, name, email, password=None):
        return self.create_user(
            phone_number,
            password=password,
            is_active=True,
            is_staff=True,
            is_admin=True,
            name=name,
            email=email,
        )

class Staff(AbstractBaseUser):
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["name", "email"]

    objects = StaffManager()

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_details(self):
        return {
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active,
            "is_staff": self.is_staff,
            "is_admin": self.is_admin,
            "id": self.id,
        }

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def f_is_active(self):
        return self.is_active

    @property
    def f_is_staff(self):
        return self.is_staff

    @property
    def f_is_admin(self):
        return self.is_admin
