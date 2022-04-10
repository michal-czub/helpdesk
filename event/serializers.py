from rest_framework import serializers
from event.models import Event
from datetime import timezone
from application.serializers import ApplicationSerializer
from consultation.serializers import ConsultationSerializer
from stage.serializers import StageSerializer
# from client.serializers import ClientSerializer

# list for staff
# # signature, client, created_at, app, functionality, subject, has_attachment(attachment=False/True),
# # staff
class StaffListEventSerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField()
    application = serializers.SerializerMethodField()  # jedna na event
    #staff = serializers.SerializerMethodField(allow_null=True)
    stage = serializers.SerializerMethodField()
    signature = serializers.CharField(read_only=True)
    has_attachment = serializers.SerializerMethodField(read_only=True)

    def get_stage(self, instance):
        return instance.get_stage_name()

    def get_client(self, instance):
        return instance.get_client_name()

    def get_application(self, instance):
        return instance.get_app_name()

    # def get_staff(self, instance):
    #     return instance.get_staff_details()

    def get_has_attachment(self, instance):
        return instance.has_attachment()

    class Meta:
        model = Event
        fields = (
            "id",
            "url",
            "signature",
            "stage",
            "created_at",
            "functionality",
            "subject",
            "has_attachment",
            "client",
            "application",
            "staff",
        )

# details for staff
class StaffRetrieveEventSerializer(serializers.ModelSerializer):
    signature = serializers.CharField(read_only=True)
    reported_at = serializers.DateTimeField(read_only=True)
    finished_at = serializers.DateTimeField(allow_null=True)
    subject = serializers.CharField(read_only=True)
    # stage = serializers.SerializerMethodField()
    description = serializers.CharField(read_only=True)
    assigned_by = serializers.SerializerMethodField(read_only=True)
    staff_name = serializers.SerializerMethodField()
    app_name = serializers.SerializerMethodField()
    #consultation = serializers.SerializerMethodField()
    consultations = ConsultationSerializer(many=True, read_only=True)

    def get_staff_name(self, instance):
        return instance.get_staff_name()

    def get_app_name(self, instance):
        return instance.get_app_name()

    def get_assigned_by(self, instance):
        return instance.get_client_details()

    # def get_stage(self, instance):
    #     return instance.get_stage_name()

    # def get_consultation(self, instance):
    #     return (consultation.get_details() for consultation in instance.consultations.all())

    class Meta:
        model = Event
        fields = (
            "id",
            "url",
            "signature",
            "reported_at",
            "finished_at",
            "status",
            "priority",
            "staff",
            "staff_name",
            "stage",
            # "stages",
            "board",
            "app",
            "app_name",
            "functionality",
            "subject",
            "description",
            "attachment",
            # Send by:
            "assigned_by",
            # Consultation:
            # "consultation",
            "consultations",
            # Asana:
            "is_assana_integrated",
        )

class CreateEventSerializer(serializers.ModelSerializer):
    key = serializers.CharField(style={"input_type": "password"}, write_only=True)
    consultation_date = serializers.DateTimeField(write_only=True, allow_null=True)
    reported_at = serializers.DateTimeField(read_only=True)
    stages = StageSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = (
            "app",
            "subject",
            "functionality",
            "description",
            "attachment",
            "reported_at",
            "stages",
            "key",
            "consultation_date",
        )

    def create(self, validated_data):
        validated_data.pop("key")
        validated_data.pop("consultation_date")
        # import pdb; pdb.set_trace()
        return Event.objects.create(**validated_data)

class ClientListEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ()

class ClientRetrieveEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ()
