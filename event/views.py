import random
import string
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated  # dodać własne z is_staff
from rest_framework.decorators import action
from event.models import Event
from stage.models import Stage
from client.models import Client
import datetime
from event.serializers import (StaffListEventSerializer, StaffRetrieveEventSerializer,
                               ClientListEventSerializer, ClientRetrieveEventSerializer,
                               CreateEventSerializer)

#@require_http_methods(["GET", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"])
class StaffEventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "put", "patch", "delete", "options", "head"]

    # @action(detail=True, methods=["put", "patch"])
    # def task_finished(self):
    def perform_update(self, serializer):
        instance = self.get_object()
        if self.request.data["status"] == "resolved" and self.request.user.is_authenticated:
            updated_instance = serializer.save(finished_at=datetime.datetime.now())
        elif self.request.data["status"] == "in_progress" and self.request.user.is_authenticated:
            serializer.save(finished_at=None)
        else:
            serializer.save(finished_at=None)
        # TODO:  wysłanie powiadomienia do klienta na endpoint
        # TODO:  dorobienie obsługi Konsultacji telefonicznej
        # TODO:  assana
        # TODO:  filtry i searchfield
        # TODO:  testy do modeli

    def get_serializer_class(self):
        if self.action == "list":
            return StaffListEventSerializer
        elif self.action == "retrieve" or self.action == "put" or self.action == "delete":
            return StaffRetrieveEventSerializer
        return StaffRetrieveEventSerializer  # todo: ?

class ClientEventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = CreateEventSerializer
    # permission_classes = # todo: Tylko client może tworzyć nowe zgłoszenia

    def perform_create(self, serializer):
        today = datetime.date.today()
        client = Client.objects.get(key=self.request.data["key"])  # TODO 3: Dodać walidację (co gdy nie matchuje)
        stage = Stage.objects.get(name="Nowe")
        serializer.save(signature="Z {number}/{month}/{year}/{letter}".format(number=random.randrange(0, 99),
                                                                              month=today.month, year=today.year,
                                                                              letter=random.choice(
                                                                                  string.ascii_uppercase)),
                        stage=stage, reported_at=datetime.datetime.now(), client=client)
        # if Stage.objects.get(name="Nowe").exists() and Client.objects.get(key=self.request.data["key"]):
        #     stage = Stage.objects.get(name="Nowe")  # TODO 4: Dodać walidację (co gdy nie istnieje)
        #     client = Client.objects.get(key=self.request.data["key"])
        #     serializer.save(signature="Z {number}/{month}/{year}/{letter}".format(number=random.randrange(0, 99),
        #                                                                           month=today.month, year=today.year,
        #                                                                           letter=random.choice(
        #                                                                               string.ascii_uppercase)),
        #                     stage=stage, reported_at=datetime.datetime.now(), client=client)
        # elif Client.objects.get(key=self.request.data["key"]):
        #     client = Client.objects.get(key=self.request.data["key"])
        #     serializer.save(signature="Z {number}/{month}/{year}/{letter}".format(number=random.randrange(0, 99),
        #                                                                           month=today.month, year=today.year,
        #                                                                           letter=random.choice(
        #                                                                               string.ascii_uppercase)),
        #                     reported_at=datetime.datetime.now(), client=client)
