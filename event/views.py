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
from event.serializers import (StaffListEventSerializer, StaffRetrieveEventSerializer,
                               ClientListEventSerializer, ClientRetrieveEventSerializer,
                               CreateEventSerializer)

class StaffEventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]
    #http_method_names = ["get", "put", "patch", "delete", "options", "head", "post"]

    # @action(detail=True, methods=["put", "patch"])
    # def task_finished(self):
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
            url = self.request.data#.assigned_by.url_message
            import pdb; pdb.set_trace()
            payload = {"status": self.request.data["status"], "info": "Ticket closed",
                       "status_changed_by": self.request.user, "date": datetime.datetime.now()}
            head = {'Authorization': 'Bearer {}'.format(myToken)}
            requests.post(url_message, data=payload, headers=head)
            serializer.save(finished_at=datetime.datetime.now())
        elif self.request.data["status"] == "in_progress" and self.request.user.is_authenticated:
            #url = self.request.data["assigned_by.url_message"]
            payload = {"status": self.request.data["status"], "info": "Your ticket is being processed",
                       "status_changed_by": self.request.user, "date": datetime.datetime.now()}
            head = {'Authorization': 'Bearer {}'.format(myToken)}
            # 9a53c90d-39a3-4d46-a143-7ec5a450c24a
            requests.post("http://127.0.0.1:8000/message/", data=payload, headers=head)
            serializer.save(finished_at=None)
        else:
            serializer.save(finished_at=None)
        # TODO:  wysłanie powiadomienia do klienta na endpoint [o zakończenie / zmianie statusu eventu]
        # TODO:  dorobienie obsługi Konsultacji telefonicznej
        # TODO:  assana
        # TODO:  filtry i searchfield
        # TODO:  testy do modeli
        # TODO:  widoki dla clienta - lista jego zleceń i szczegółowy widok zlecenia

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
