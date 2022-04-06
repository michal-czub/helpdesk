from rest_framework import serializers
from stage.models import Stage
#from event.serializers import StaffListEventSerializer

class StageSerializer(serializers.ModelSerializer):
    event = serializers.SerializerMethodField(read_only=True)
    #events = StaffListEventSerializer(many=True)

    # def get_board(self, instance):
    #   return (board.get_details() for board in instance.boards.all())
    def get_event(self, instance):
        return (event.get_shortened_details() for event in instance.events.all())

    class Meta:
        model = Stage
        fields = (
            "id",
            "url",
            "name",
            "order",
            "board",
            "events",
            "event",
        )
