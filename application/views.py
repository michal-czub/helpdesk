from django.shortcuts import render
from rest_framework import viewsets
from application.models import Application
from application.serializers import ApplicationSerializer

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.select_related("project").all()
    serializer_class = ApplicationSerializer
