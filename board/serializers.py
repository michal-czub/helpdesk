from rest_framework import serializers
from board.models import Board

class BoardSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()

    def get_project(self, instance):
        return instance.get_project_details()

    class Meta:
        model = Board
        fields = (
            "id",
            "url",
            "name",
            "project",
        )
