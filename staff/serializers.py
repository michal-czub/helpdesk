from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from staff.models import Staff
from team.serializers import TeamSerializer

class StaffSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many=True)

    class Meta:
        model = Staff
        fields = (
            "id",
            "url",
            "name",
            "email",
            "phone_number",
            "is_active",
            "is_staff",
            "teams",
        )

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password],
                                     style={"input_type": "password"})
    is_active = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        user = Staff.objects.create(
            phone_number=validated_data["phone_number"],
            name=validated_data["name"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()

        return user

    class Meta:
        model = Staff
        fields = [
            "phone_number",
            "password",
            "name",
            "email",
            "is_active",
            "is_staff",
        ]

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["phone_number"] = str(user.phone_number)
        return token
