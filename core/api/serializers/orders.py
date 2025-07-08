from rest_framework import serializers
from api.models import Product
from api.services import ProductService, CartService


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, max_length=500)
    original_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    selling_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    inventory_count = serializers.IntegerField()
    image_url = serializers.URLField(required=False, allow_blank=True)
    image_url_list = serializers.JSONField(required=False)
    is_in_stock = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["in_stock"] = instance.is_in_stock
        return representation


class CartItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    product = serializers.UUIDField(write_only=True)
    product_id = serializers.UUIDField(source="product.id", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_price = serializers.DecimalField(
        source="product.price", max_digits=10, decimal_places=2, read_only=True
    )
    product_image_url = serializers.URLField(source="product.image_url", read_only=True)
    quantity = serializers.IntegerField(min_value=1)
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    def validate_product(self, value):
        try:
            ProductService.get_product_by_id(value)
        except:
            raise serializers.ValidationError("Product not found")
        return value

    def validate(self, data):
        product_id = data.get("product")
        quantity = data.get("quantity")

        if product_id and not ProductService.check_product_availability(
            product_id, quantity
        ):
            product = ProductService.get_product_by_id(product_id)
            raise serializers.ValidationError(
                f"Quantity ({quantity}) exceeds available stock ({product.inventory_count})"
            )
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        product_id = validated_data["product"]
        quantity = validated_data["quantity"]
        return CartService.add_to_cart(user, str(product_id), quantity)

    def update(self, instance, validated_data):
        user = self.context["request"].user
        quantity = validated_data.get("quantity", instance.quantity)
        return CartService.update_cart_item(user, str(instance.id), quantity)


class CartItemUpdateSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)

    def validate_quantity(self, value):
        cart_item = self.instance
        if cart_item and value > cart_item.product.inventory_count:
            raise serializers.ValidationError(
                f"Quantity ({value}) exceeds available stock ({cart_item.product.inventory_count})"
            )
        return value

    def update(self, instance, validated_data):
        user = self.context["request"].user
        quantity = validated_data["quantity"]
        return CartService.update_cart_item(user, str(instance.id), quantity)
