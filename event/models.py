from django.db import models
from staff.models import Staff
from client.models import Client
import uuid

class Event(models.Model):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"

    STATUS_CHOICES = (
        (NEW, "New"),
        (IN_PROGRESS, "In progress"),
        (RESOLVED, "Event resolved"),
    )

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    PRIORITY_CHOICES = (
        (LOW, "Low"),
        (MEDIUM, "Medium"),
        (HIGH, "High"),
    )

    ACCOUNTANCY = "accountancy"
    PEOPLE = "people"
    PRODUCTION = "production"
    PRODUCTS = "products"
    WAREHOUSE = "warehouse"
    REPORT = "report"
    TRANSPORT = "transport"
    ORDERS_AND_COMPLAINTS = "orders_and_complaints"

    FUNCTIONALITY_CHOICES = (
        (ACCOUNTANCY, "Accountancy"),
        (PEOPLE, "People"),
        (PRODUCTION, "Production"),
        (PRODUCTS, "Products"),
        (WAREHOUSE, "Warehouse"),
        (REPORT, "Report"),
        (TRANSPORT, "Transport"),
        (ORDERS_AND_COMPLAINTS, "Orders and complaints"),
    )

    NEW_FEATURE = "I need a new feature"
    HELP = "I need help"
    REMARK = "I have remarks about application"
    ERROR = "Bug in application"

    SUBJECT_CHOICES = (
        (NEW_FEATURE, "I need a new feature"),
        (HELP, "I need help"),
        (REMARK, "I have remarks about application"),
        (ERROR, "Bug in application"),
    )

    BUG = "bug"
    FEATURE = "feature"
    IMPORTANT = "important"
    CRITICAL = "critical"

    LABEL_CHOICES = (
        (BUG, "Bug"),
        (FEATURE, "Feature"),
        (IMPORTANT, "Important"),
        (CRITICAL, "Critical"),
    )

    app = models.ForeignKey(
        "application.Application",
        related_name="events",
        on_delete=models.CASCADE
    )
    # event can have no staff or team assigned
    staff = models.ForeignKey(
        "staff.Staff",
        related_name="events",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    team = models.ForeignKey(
        "team.Team",
        related_name="events",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    # deleting board means deleting events related to this board
    board = models.ForeignKey(
        "board.Board",
        related_name="events",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    # deleting stage means its events stay as a part of certain board
    stage = models.ForeignKey(
        "stage.Stage",
        related_name="events",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    client = models.ForeignKey(
        "client.Client",
        related_name="events",
        on_delete=models.CASCADE
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    signature = models.CharField(max_length=14)  # perform_create --> create in managers.py
    created_at = models.DateTimeField(auto_now_add=True)
    reported_at = models.DateTimeField()    # client sends timezone.now()
    finished_at = models.DateTimeField(blank=True, null=True)    # staff decides
    status = models.CharField(choices=STATUS_CHOICES, default=NEW, max_length=255)
    functionality = models.CharField(choices=FUNCTIONALITY_CHOICES, blank=True, max_length=255)
    subject = models.CharField(choices=SUBJECT_CHOICES, max_length=255)
    priority = models.CharField(choices=PRIORITY_CHOICES, blank=True, max_length=255)
    label = models.CharField(choices=LABEL_CHOICES, blank=True, max_length=255)
    description = models.CharField(max_length=500, default="")
    attachment = models.FileField(blank=True)
    is_assana_integrated = models.BooleanField(default=False)

    def __str__(self):
        return self.signature

    def get_client_name(self):
        return self.client.get_name()

    def get_client_details(self):
        return self.client.get_details()

    def get_stage_name(self):
        return self.stage.get_name() if self.stage else None

    def get_app_name(self):
        return self.app.get_name()

    def get_staff_name(self):
        return self.staff.name if self.staff else None

    def get_staff_details(self):
        return self.staff.get_details() if self.staff else None

    def has_attachment(self):
        return True if self.attachment else False

    def get_shortened_details(self):
        return {
            "id": self.id,
            "signature": self.signature,
            "created_at": self.created_at,
            "client_name": self.get_client_name(),
            "app": self.get_app_name(),
            "subject": self.subject,
            "functionality": self.functionality,
            "staff": self.get_staff_details(),
        }

    def get_all_details(self):
        return {
            "id": self.id,
            "signature": self.signature,
            "created_at": self.created_at,
            "app": self.get_app_name(),
            "subject": self.subject,
            "functionality": self.functionality,
            "staff": self.get_staff_details(),
            "reported_at": self.reported_at,
            "finished_at": self.finished_at,
            "status": self.status,
            "priority": self.priority,
            "label": self.label,
            "description": self.description,
            "attachment": self.attachment,
            "is_assana_integrated": self.is_assana_integrated,
            "client": self.client,
            "board": self.board,
        }

    def get_details_for_course(self):
        return {
            "id": self.id,
            "signature": self.signature,
        }

class Course(models.Model):
    event = models.ForeignKey(
        "event.Event",
        related_name="courses",
        on_delete=models.CASCADE
    )
    client = models.ForeignKey(
        "client.Client",
        related_name="courses",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    staff = models.ForeignKey(
        "staff.Staff",
        related_name="courses",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    message = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(blank=True)

    def get_event_details(self):
        return self.event.get_details_for_course()

    def get_client_name(self):
        return self.client.__str__()

    def get_staff_name(self):
        return self.staff.__str__()

    class Meta:
        ordering = [
            "-created_at"
        ]
