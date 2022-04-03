from rest_framework import serializers
from project.models import Project
from board.serializers import BoardSerializer

class ProjectSerializer(serializers.ModelSerializer):
    #board = serializers.SerializerMethodField()
    boards = BoardSerializer(many=True, read_only=True)
    # def get_board(self, instance):
    #     return (board.get_details() for board in instance.boards.all())

    class Meta:
        model = Project
        fields = (
            "id",
            "url",
            "name",
            "boards",
        )
