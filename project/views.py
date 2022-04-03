from django.shortcuts import render
from rest_framework import viewsets
from project.models import Project
from project.serializers import ProjectSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
