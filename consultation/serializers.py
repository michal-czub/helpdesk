from rest_framework import serializers
from consultation.models import Consultation

class ConsultationSerializer(serializers.ModelSerializer):

    client = serializers.SerializerMethodField(read_only=True)

    def get_client(self, instance):
        return instance.get_client_details()

    class Meta:
        model = Consultation
        fields = (
            "id",
            "url",
            "date",
            "is_confirmed",
            "client",
        )
