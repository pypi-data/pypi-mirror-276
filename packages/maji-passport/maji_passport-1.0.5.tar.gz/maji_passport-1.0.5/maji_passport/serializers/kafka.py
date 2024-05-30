from rest_framework.fields import BooleanField, CharField, JSONField
from rest_framework.serializers import Serializer

from maji_passport.utils import clear_phone_number, get_passport_user_serializer
from maji_passport.models import PassportUser
from django.contrib.auth import get_user_model

CustomSerializer = get_passport_user_serializer()
User = get_user_model()


class PassportUserDataSerializer(Serializer):
    avatar_url = CharField(required=False, allow_blank=True, allow_null=True)
    cover_url = CharField(required=False, allow_blank=True, allow_null=True)
    display_name = CharField(required=False, allow_blank=True)
    social_networks = JSONField(required=False)


class KafkaUpdateUserSerializer(CustomSerializer):
    """
    Serializer for kafka update user messages

    phone and is_phone_verified is read_only_fields in ArgoUserDetailsSerializer
    and here we must declare them read_only=False and required=False
    """

    phone = CharField(read_only=False, required=False, allow_blank=True)
    is_phone_verified = BooleanField(read_only=False, required=False)

    user_data = PassportUserDataSerializer(required=False)

    class Meta(CustomSerializer.Meta):
        fields = CustomSerializer.Meta.fields + ("user_data",)

    def validate_phone(self, value):
        return clear_phone_number(value)

    def update(self, instance, validated_data):
        """
        If we get a phone number in data, this means that the user has changed phone
        in the passport and needs to update it for the current user
        and remove it from other users, who have that phone
        """
        if "phone" in validated_data and validated_data["phone"]:
            old_users = User.objects.filter(phone=validated_data["phone"])
            old_users.update(phone="", is_phone_verified=False)
        if "user_data" in validated_data:
            # update PassportUser data for this user
            PassportUser.objects.filter(argo_user=instance).update(
                **validated_data["user_data"]
            )
        return super().update(instance, validated_data)
