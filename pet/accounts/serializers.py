from rest_framework import serializers

from .models import CustomUser, MailingList


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "city",
            "email",
            "send_status_email",
        ]
        read_only_fields = ["id", "email", "send_status_email"]


class MailingListSerializer(serializers.ModelSerializer):

    class Meta:
        model = MailingList
        fields = [
            "email",
            "send_ads_email",
        ]

        read_only_fields = ["send_ads_email"]
