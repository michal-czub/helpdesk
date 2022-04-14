from django.shortcuts import render
from rest_framework import viewsets
from board.models import Board
from board.serializers import BoardSerializer

class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.select_related("project").all()
    serializer_class = BoardSerializer
