from django.db import models
from staff.models import Staff
from team.models import Team
from application.models import Application
from board.models import Board
from stage.models import Stage
from client.models import Client
import uuid

class Event(models.Model):
    app = models.ForeignKey(Application, related_name="events", on_delete=models.CASCADE)
    # event może nie mieć przypisanego pracownika / zespołu
    staff = models.ForeignKey(Staff, related_name="events", on_delete=models.SET_NULL, null=True, blank=True)
    team = models.ForeignKey(Team, related_name="events", on_delete=models.SET_NULL, null=True, blank=True)
    # usuwając board -> usuwamy eventy w boardzie
    board = models.ForeignKey(Board, related_name="events", on_delete=models.CASCADE)
    # usuwając stage, event nadal jest częścią danego board'a
    stage = models.ForeignKey(Stage, related_name="events", on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(Client, related_name="events", on_delete=models.CASCADE)
    # assigned_to = models.ManyToManyField(Staff, related_name="events")

    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"

    STATUS = [
        (NEW, "New"),
        (IN_PROGRESS, "In progress"),
        (RESOLVED, "Event resolved"),
    ]

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    ACCOUNTANCY = "accountancy"
    PEOPLE = "people"
    PRODUCTION = "production"
    PRODUCTS = "products"
    WAREHOUSE = "warehouse"
    REPORT = "report"
    TRANSPORT = "transport"
    ORDERS_AND_COMPLAINTS = "orders_and_complaints"

    FUNCTIONALITY = [
        (ACCOUNTANCY, "Accountancy"),
        (PEOPLE, "People"),
        (PRODUCTION, "Production"),
        (PRODUCTS, "Products"),
        (WAREHOUSE, "Warehouse"),
        (REPORT, "Report"),
        (TRANSPORT, "Transport"),
        (ORDERS_AND_COMPLAINTS, "Orders and complaints"),
    ]

    NEW_FEATURE = "feature"
    HELP = "help"
    REMARK = "remark"
    ERROR = "error"

    SUBJECT = [
        (NEW_FEATURE, "I need a new feature"),
        (HELP, "I need help"),
        (REMARK, "I have remarks about application"),
        (ERROR, "Bug in application"),
    ]

    PRIORITY = [
        (LOW, "Low"),
        (MEDIUM, "Medium"),
        (HIGH, "High"),
    ]

    BUG = "bug"
    FEATURE = "feature"
    IMPORTANT = "important"
    CRITICAL = "critical"

    LABEL = [
        (BUG, "Bug"),
        (FEATURE, "Feature"),
        (IMPORTANT, "Important"),
        (CRITICAL, "Critical"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    signature = models.CharField(max_length=14)  # perform_create
    created_at = models.DateTimeField(auto_now_add=True)
    reported_at = models.DateTimeField()    # client sends timezone.now()
    finished_at = models.DateTimeField(blank=True)    # staff decides
    status = models.CharField(choices=STATUS, default=NEW, max_length=255)
    functionality = models.CharField(choices=FUNCTIONALITY, blank=True, max_length=255)
    subject = models.CharField(choices=SUBJECT, max_length=255)
    priority = models.CharField(choices=PRIORITY, blank=True, max_length=255)
    label = models.CharField(choices=LABEL, blank=True, max_length=255)
    description = models.CharField(max_length=500, default="")
    attachment = models.FileField(blank=True)  # upload_to
    is_assana_integrated = models.BooleanField(default=False)
