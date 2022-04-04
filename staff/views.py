from django.shortcuts import render
from django.http import Http404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, generics
from staff.models import Staff
from staff.serializers import (StaffSerializer, MyTokenObtainPairSerializer, RegisterSerializer)

class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class StaffRegisterView(generics.CreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

class MyAccountViewSet(APIView):
    def get(self, request, pk=None):
        staff = Staff.objects.get(id=request.user.id)
        serializer_context = {
            'request': request,
        }
        serializer = StaffSerializer(staff, context=serializer_context)
        return Response(serializer.data)
