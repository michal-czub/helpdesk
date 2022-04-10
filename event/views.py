import random
import string
import datetime
import asana
import requests
from requests_jwt import JWTAuth
from django.utils.datastructures import MultiValueDictKeyError
from django.utils import timezone
from datetime import timedelta
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (IsAuthenticated, AllowAny)  # dodać własne z is_staff
from rest_framework.decorators import action
from django_filters import rest_framework as filters
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


class AsanaViewSet(ModelViewSet):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = StaffRetrieveEventSerializer


class MyEventViewSet(ModelViewSet):
    serializer_class = StaffListEventSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EventFilter

    def get_queryset(self):
        return Event.objects.filter(staff=self.request.user)


class StaffEventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EventFilter

    def perform_update(self, serializer):
        instance = self.get_object()
        # url klienta na który ma pójść message
        test = instance._meta.get_fields()[6].value_from_object(instance)
        # value = test[6].value_from_object(instance)
        client = Client.objects.get(id=test)
        url_message = client._meta.get_fields()[-1].value_from_object(client)
        # value2 = test2[-1].value_from_object(client)
        myToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5NTI4OTU0LCJpYXQiOjE2NDkzNTYxNTQsImp0aSI6ImEzM2Y2NWQyM2EwNzQwMzFhMWExODYxYTlkNzY0OWZkIiwidXNlcl9pZCI6IjFiOWM1Y2FhLTcwMzQtNDg2OS1hNWRhLTg3NWMzYjg4NzgyZCIsInBob25lX251bWJlciI6Iis0ODYwOTIwMDUwMCJ9.D0G9jQxdPe9qjN7cijpAHBJiaAWdUpyw7hQ1ewKnM30"
        if self.request.data["status"] == "resolved" and self.request.user.is_authenticated:
            payload = {"status": self.request.data["status"], "info": "Ticket closed",
                       "status_changed_by": self.request.user, "date": datetime.datetime.now()}
            head = {'Authorization': 'Bearer {}'.format(myToken)}
            requests.post(url_message, data=payload, headers=head)
            #serializer.save(finished_at=datetime.datetime.now())
            serializer.save()
        elif self.request.data["status"] == "in_progress" and self.request.user.is_authenticated:
            payload = {"status": self.request.data["status"], "info": "Your ticket is being processed",
                       "status_changed_by": self.request.user, "date": datetime.datetime.now()}
            head = {'Authorization': 'Bearer {}'.format(myToken)}
            requests.post(url_message, data=payload, headers=head)
            # serializer.save(finished_at=None)
            serializer.save()
        else:
            #serializer.save(finished_at=None)
            serializer.save()
        try:
            if self.request.data["is_assana_integrated"] and self.request.user.is_authenticated:
                personal_access_token = ""
                header_asana = {'Authorization': f'Bearer {personal_access_token}'}
                asana_client = asana.Client.access_token(personal_access_token)
                workspace_id = asana_client.users.me()['workspaces'][0]['gid']

                # GET PROJECT ID =================================
                get_projects_url = f"https://app.asana.com/api/1.0/projects/?workspace={workspace_id}"
                projects = requests.get(get_projects_url, headers=header_asana)
                for data in projects.json()["data"]:
                    if data["name"] == "helpdesk":
                        project_id = data["gid"]
                # =================================================

                # SEARCH FOR SECTION / STAGE AND CREATE NEW STAGE =
                sections_url = f"https://app.asana.com/api/1.0/projects/{project_id}/sections"
                get_sections = requests.get(sections_url, headers=header_asana)
                section_flag = False
                if instance.stage is not None:
                    print("instance stage jest OK")
                    for section in get_sections.json()["data"]:
                        if section["name"] == instance.stage.name:
                            print("juz istnieje taki stage")
                            section_flag = True
                            break
                if section_flag is False and instance.stage is not None:
                    payload_create_section = {
                        "name": instance.stage,
                    }
                    requests.post(sections_url, data=payload_create_section, headers=header_asana)
                    print(f"postuje sekcje {instance.stage}")

                # =================================================

                # CREATE TASK FOR PROJECT =========================
                # due_at = instance.finished_at if instance.finished_at else
                if instance.finished_at:
                    due_at = instance.finished_at
                else:
                    due_at = None
                current_time = datetime.datetime.now()
                if instance.finished_at:
                    # timedelta - server (2h)
                    finish_due = (instance.finished_at - timedelta(hours=2)).isoformat()
                elif self.request.data["finished_at"]:
                    print("pobieram datę z self.request.data")
                    temp = datetime.datetime.strptime(self.request.data["finished_at"], "%Y-%m-%dT%H:%M").isoformat()
                    finish_due = datetime.datetime.strptime(temp, "%Y-%m-%dT%H:%M:%S")-timedelta(seconds=0.1)
                    # finish_due = finish_due.isoformat()
                    # finish_due = datetime.datetime.strptime(self.request.data["finished_at"], "%Y-%m-%dT%H:%M:%S")
                    #finish_due = self.request.data["finished_at"]
                else:
                    print("Ustawiam finish-due -> None")
                    finish_due = None
                payload_create_task = {
                        "projects": project_id,
                        "name": instance.signature,
                        "assignee": asana_client.users.me()['gid'],
                        #"notes": "przykladowy opis",
                        "notes": f"Task added on: {instance.reported_at}\n"
                                 f"Clients description: {instance.description}\n"
                                 f"Subject: {instance.subject}\n"
                                 f"Functionality: {instance.functionality}\n"
                                 f"Application: {instance.app.name}\n"                                 
                                 f"Status: {instance.status}\n"
                                 f"Priority: {instance.priority}\n"
                                 f"Board: {instance.board}\n"
                                 f"Stage: {instance.stage}\n"
                                 #f"Staff member assigned: {instance.staff.name}\n\n"
                                 f"Client: {instance.client.name}\n"
                                 f"Company: {instance.client.company}\n"
                                 f"Phone number: {instance.client.phone_number}\n"
                                 f"Email: {instance.client.email}\n\n",
                                 # f"Consultation details: {instance.consultations.}",
                        "due_at": finish_due,
                        # "start_at": "2022-09-15T02:06:58.147Z"
                }
                # Check if task with same signature exists: (if so -> don't send)
                task_flag = False
                get_tasks = requests.get(f"https://app.asana.com/api/1.0/tasks/?project={project_id}&start_at={current_time}",
                                         headers=header_asana)
                for task in get_tasks.json()["data"]:
                    if task["name"] == instance.signature:
                        task_flag = True
                        print("task name taki sam jak instance signature")
                        break

                if instance.stage is not None and task_flag is not True:
                    print("instance stage jest ok ")
                    get_sections = requests.get(sections_url, headers=header_asana)
                    for section in get_sections.json()["data"]:
                        if section["name"] == instance.stage.name:
                            section_id = section["gid"]
                            requests.post(f"https://app.asana.com/api/1.0/tasks/?assignee_section={section_id}",
                                          data=payload_create_task, headers=header_asana)
                        # else:
                        #     requests.post(f"https://app.asana.com/api/1.0/tasks",
                        #                   data=payload_create_task, headers=header_asana)
                elif instance.stage is None and task_flag is not True:
                    print("Wysyłam bez sekcji")
                    requests.post(f"https://app.asana.com/api/1.0/tasks",
                                  data=payload_create_task, headers=header_asana)
                    # ?start_at = {current_time}
                # ==================================================
                # import pdb; pdb.set_trace()
        except MultiValueDictKeyError:
            serializer.save(is_assana_integrated=False)
            # elif self.request.data["is_assana_integrated"] is False and self.request.user.is_authenticated:
            #     print("Jestem w elif is assana integrated is False")
            #     import pdb; pdb.set_trace()
            #     serializer.save(is_assana_integrated=False)

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
    permission_classes = [AllowAny,]

    def perform_create(self, serializer):
        # instance = self.get_object()
        today = datetime.date.today()
        client = Client.objects.get(key=self.request.data["key"])  # TODO 3: Dodać walidację (co gdy nie matchuje)
        # stage = Stage.objects.get(name="Nowe")
        if Stage.objects.get(name="Nowe"):
            stage = Stage.objects.get(name="Nowe")
        else:
            stage = None
        event = serializer.save(signature="Z {number}/{month}/{year}/{letter}".format(number=random.randrange(0, 99),
                                                                                      month=today.month,
                                                                                      year=today.year,
                                                                                      letter=random.choice(
                                                                                          string.ascii_uppercase)),
                                reported_at=datetime.datetime.now(), client=client, stage=stage)
        if self.request.data["consultation_date"]:
            Consultation.objects.create(date=self.request.data["consultation_date"], is_confirmed=False, client=client,
                                        event=event)
