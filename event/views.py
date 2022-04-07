import random
import string
import datetime
import requests
from requests_jwt import JWTAuth
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated  # dodać własne z is_staff
from rest_framework.decorators import action
from event.models import Event
from stage.models import Stage
from client.models import Client
from consultation.models import Consultation
from event.serializers import (StaffListEventSerializer, StaffRetrieveEventSerializer,
                               ClientListEventSerializer, ClientRetrieveEventSerializer,
                               CreateEventSerializer)

class StaffEventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]

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
            requests.post("http://127.0.0.1:8000/message/", data=payload, headers=head)
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
        serializer.save(signature="Z {number}/{month}/{year}/{letter}".format(number=random.randrange(0, 99),
                                                                              month=today.month, year=today.year,
                                                                              letter=random.choice(
                                                                                  string.ascii_uppercase)),
                        reported_at=datetime.datetime.now(), client=client)
        import pdb; pdb.set_trace()
        Consultation.objects.create(date=datetime.datetime.now(), is_confirmed=False, client=client)
