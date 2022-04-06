from django.shortcuts import render
from client.models import Client
from client.serializers import ClientSerializer
from rest_framework.viewsets import ModelViewSet

class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
