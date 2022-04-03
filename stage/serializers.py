from rest_framework import serializers
from stage.models import Stage

class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = (
            "id",
            "url",
            "name",
            "order",
            "board",
        )
