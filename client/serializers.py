from abc import ABC

from rest_framework import serializers
from client.models import Client

class ClientSerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField(read_only=True)
    url_message = serializers.URLField(read_only=True)
    key = serializers.CharField(style={"input_type": "password"}, write_only=True)

    def get_events(self, instance):
        return (event.get_shortened_details() for event in instance.events.all())

    class Meta:
        model = Client
        fields = (
            "id",
            "url",
            "url_message",
            "phone_number",
            "email",
            "name",
            "company",
            "events",
            "key",
        )

# class Message(object):
#     def __init__(self, status, info):
#         self.status = status
#         self.info = info
#
# class MessageSerializer(serializers.Serializer):
#     status = serializers.CharField()
#     info = serializers.CharField()

    # class Meta:
    #     fields = (
    #         "status",
    #         "info",
    #     )
