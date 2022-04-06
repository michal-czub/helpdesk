from django.shortcuts import render
from rest_framework import viewsets
from stage.models import Stage
from stage.serializers import StageSerializer

class StageViewSet(viewsets.ModelViewSet):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
