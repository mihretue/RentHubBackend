from rest_framework import serializers
from apps.Users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "email_verified",
            "image",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "email_verified", "created_at", "updated_at"]


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
            "status",
            "phone_number",
            "is_verified",
            "image",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)  # hash the password
        user.save()
        return user
