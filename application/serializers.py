from rest_framework import serializers
from application.models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            "id",
            "url",
            "name",
            "project",
        )
