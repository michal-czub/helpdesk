from rest_framework import serializers
from board.models import Board
from stage.serializers import StageSerializer

class BoardSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField()
    stages = StageSerializer(many=True, read_only=True)

    def get_projects(self, instance):
        return instance.get_project_details()

    class Meta:
        model = Board
        fields = (
            "id",
            "url",
            "name",
            "project",
            "projects",
            "stages",
        )
