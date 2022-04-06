from rest_framework import serializers
from event.models import Event
from datetime import timezone
from application.serializers import ApplicationSerializer
from stage.serializers import StageSerializer
# from client.serializers import ClientSerializer

# list for staff
# # signature, client, created_at, app, functionality, subject, has_attachment(attachment=False/True),
# # staff
class StaffListEventSerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField() # client name todo only
    application = serializers.SerializerMethodField() # jedna na event
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

# TODO 1: Defaultowy stage dla nowopowstałego eventu
# TODO 2:

# details for staff
class StaffRetrieveEventSerializer(serializers.ModelSerializer):
    signature = serializers.CharField(read_only=True)
    reported_at = serializers.DateTimeField(read_only=True)
    finished_at = serializers.DateTimeField(read_only=True)
    subject = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    assigned_by = serializers.SerializerMethodField(read_only=True)
    staff_name = serializers.SerializerMethodField()
    app_name = serializers.SerializerMethodField()

    def get_staff_name(self, instance):
        return instance.get_staff_name()

    def get_app_name(self, instance):
        return instance.get_app_name()

    def get_assigned_by(self, instance):
        return instance.get_client_details()

    #  TODO 5: ACTION - PO UPDATE'CIE STATUSU - MESSAGE NA JAKIŚ ENDPOINT ŻE ZMIANA
    #  TODO 6: ACTION - PO UPDATE'CIE STATUSU NA ZAKOŃCZONE - MESSAGE NA JAKIŚ ENDPOINT ŻE KONIEC

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
            "board",
            "app",
            "app_name",
            "functionality",
            "subject",
            "description",
            "attachment",
            # Send by:
            "assigned_by",
        )

class CreateEventSerializer(serializers.ModelSerializer):
    #client = serializers.PrimaryKeyRelatedField(queryset=clients.objects.)
    key = serializers.CharField(style={"input_type": "password"}, write_only=True)
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
            #"client",
            "reported_at",
            "stages",
            # "consultation",
            "key",
        )

    def create(self, validated_data):
        key = validated_data.pop("key")
        return Event.objects.create(**validated_data)

class ClientListEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ()

class ClientRetrieveEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ()
