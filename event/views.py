import random
import string
import datetime
import requests
from requests_jwt import JWTAuth
from django.utils import timezone
from datetime import timedelta
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated  # dodać własne z is_staff
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter#,# OrderingFilter
from event.models import Event
from stage.models import Stage
from client.models import Client
from staff.models import Staff
from application.models import Application
from consultation.models import Consultation
from event.serializers import (StaffListEventSerializer, StaffRetrieveEventSerializer,
                               ClientListEventSerializer, ClientRetrieveEventSerializer,
                               CreateEventSerializer)

class EventFilter(filters.FilterSet):
    # SEARCH-FIELD
    signature = filters.CharFilter(lookup_expr="icontains")

    # ORDERING - SORTING
    sorting = filters.OrderingFilter(
        fields=(
            ('status', 'status'),
            ('priority', 'priority'),
            ('reported_at', 'reported_at'),
        )
    )

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

    NEW_FEATURE = "I need a new feature"
    HELP = "I need help"
    REMARK = "I have remarks about application"
    ERROR = "Bug in application"

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

    # CHOICE-FIELD
    status = filters.ChoiceFilter(field_name="status", empty_label="All", choices=STATUS)
    priority = filters.ChoiceFilter(field_name="priority", empty_label="All", choices=PRIORITY)
    application = filters.ModelChoiceFilter(
        field_name="app", empty_label="All",
        queryset=Application.objects.all()
    )
    client = filters.ModelChoiceFilter(
        field_name="client", empty_label="All",
        queryset=Client.objects.all()
    )
    subject = filters.ChoiceFilter(field_name="subject", empty_label="All", choices=SUBJECT)
    reported_at = filters.NumberFilter(field_name="reported_at",
                                 method="get_past_n_weeks", label="Weeks since report")

    def get_past_n_weeks(self, queryset, field_name, value):
        time_threshold = timezone.now() - timedelta(hours=int(value))
        return queryset.filter(reported_at__gte=time_threshold)

    functionality = filters.ChoiceFilter(field_name="functionality", empty_label="All", choices=FUNCTIONALITY)
    label = filters.ChoiceFilter(field_name="label", empty_label="All", choices=LABEL)
    staff = filters.ModelChoiceFilter(
        field_name="staff", empty_label="All",
        queryset=Staff.objects.all()
    )

class StaffEventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    # filter_fields = (
    #     'status',
    #     'priority',
    #     'client',
    # )
    filterset_class = EventFilter

    def perform_update(self, serializer):
        instance = self.get_object()
        # url klienta na który ma pójść message
        test = instance._meta.get_fields()[6].value_from_object(instance)
        # value = test[6].value_from_object(instance)
        client = Client.objects.get(id=test)
        url_message = client._meta.get_fields()[-1].value_from_object(client)
        # value2 = test2[-1].value_from_object(client)
        myToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5MzI4MDc3LCJpYXQiOjE2NDkxNTUyNzcsImp0aSI6ImNlNTFlNmE3OGM5YTQzYTI5ZWI5YWMzYjBmYmQxZDhiIiwidXNlcl9pZCI6IjFiOWM1Y2FhLTcwMzQtNDg2OS1hNWRhLTg3NWMzYjg4NzgyZCIsInBob25lX251bWJlciI6Iis0ODYwOTIwMDUwMCJ9.LwmRNDbzKQZkAUqfnAOsUYR0ywfYpM9aTF1QV11Oj2I"
        if self.request.data["status"] == "resolved" and self.request.user.is_authenticated:
            payload = {"status": self.request.data["status"], "info": "Ticket closed",
                       "status_changed_by": self.request.user, "date": datetime.datetime.now()}
            head = {'Authorization': 'Bearer {}'.format(myToken)}
            requests.post(url_message, data=payload, headers=head)
            serializer.save(finished_at=datetime.datetime.now())
        elif self.request.data["status"] == "in_progress" and self.request.user.is_authenticated:
            payload = {"status": self.request.data["status"], "info": "Your ticket is being processed",
                       "status_changed_by": self.request.user, "date": datetime.datetime.now()}
            head = {'Authorization': 'Bearer {}'.format(myToken)}
            requests.post(url_message, data=payload, headers=head)
            serializer.save(finished_at=None)
        else:
            serializer.save(finished_at=None)
        # TODO:  dorobienie obsługi Konsultacji telefonicznej - Jak powiązać event z jedocześnie tworzoną konsultacją
        # TODO:  assana
        # TODO:  filtry i searchfield
        # TODO:  testy do modeli - potem
        # TODO:  widoki dla clienta - lista jego zleceń i szczegółowy widok zlecenia - potem

    def get_serializer_class(self):
        if self.action == "list":
            return StaffListEventSerializer
        elif self.action == "retrieve" or self.action == "put" or self.action == "delete":
            return StaffRetrieveEventSerializer
        return StaffRetrieveEventSerializer

class ClientEventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = CreateEventSerializer
    # permission_classes = # todo: Tylko client może tworzyć nowe zgłoszenia

    def perform_create(self, serializer):
        #instance = self.get_object()
        today = datetime.date.today()
        client = Client.objects.get(key=self.request.data["key"])  # TODO 3: Dodać walidację (co gdy nie matchuje)
        stage = Stage.objects.get(name="Nowe")
        event = serializer.save(signature="Z {number}/{month}/{year}/{letter}".format(number=random.randrange(0, 99),
                                                                              month=today.month, year=today.year,
                                                                              letter=random.choice(
                                                                                  string.ascii_uppercase)),
                                reported_at=datetime.datetime.now(), client=client)
        Consultation.objects.create(date=self.request.data["date"], is_confirmed=False, client=client, event=event)
