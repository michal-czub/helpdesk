from rest_framework import serializers
from message.models import Message

class MessageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            "status",
            "info",
            "status_changed_by",
            "date",
        )
