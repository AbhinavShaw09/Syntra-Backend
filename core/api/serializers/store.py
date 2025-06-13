from rest_framework import serializers
from api.models import Order, OrderItem
from api.service import OrderService


class OrderItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    product_id = serializers.UUIDField(source="product.id", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_image_url = serializers.URLField(source="product.image_url", read_only=True)
    quantity = serializers.IntegerField(read_only=True)
    unit_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    total_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    status = serializers.CharField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class OrderCreateSerializer(serializers.Serializer):
    def create(self, validated_data):
        user = self.context["request"].user
        return OrderService.create_order_from_cart(user)


class OrderStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.StatusChoices.choices)

    def update(self, instance, validated_data):
        user = self.context["request"].user
        status = validated_data["status"]
        return OrderService.update_order_status(user, str(instance.id), status)
