from rest_framework import serializers

from api.models import BuyerAddress


class BuyerAddressSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    first_name = serializers.CharField(max_length=100)
    middle_name = serializers.CharField(
        max_length=100, allow_blank=True, required=False, allow_null=True
    )
    last_name = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=20)
    address_line1 = serializers.CharField(max_length=255)
    address_line2 = serializers.CharField(
        max_length=255, allow_blank=True, required=False, allow_null=True
    )
    city = serializers.CharField(max_length=50)
    country = serializers.CharField(max_length=50)

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return BuyerAddress.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
