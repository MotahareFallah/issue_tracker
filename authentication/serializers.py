from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers

from .models import OneTimeLink, OtpCode, Section, User


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ["id", "name"]


class UserSerializer(BaseUserSerializer):
    department = SectionSerializer(required=False)

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ["id", "phone", "staff_member", "is_active", "section"]


class OtpRequestSerializer(serializers.ModelSerializer):
    class Meta(serializers.ModelSerializer):
        model = OtpCode
        fields = []


class OneTimeLinkSerializer(serializers.ModelSerializer):
    model = OneTimeLink
    fields = []
