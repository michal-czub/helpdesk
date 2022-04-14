from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from consultation.models import Consultation
from consultation.serializers import ConsultationSerializer

class ConsultationViewSet(ModelViewSet):
    queryset = Consultation.objects.select_related("event", "client").all()
    serializer_class = ConsultationSerializer
    permission_classes = [IsAuthenticated]
