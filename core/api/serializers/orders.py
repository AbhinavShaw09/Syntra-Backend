from rest_framework import serializers
from api.services import ProductService, CartService


class CartItemSerializer(serializers.Serializer):
    product = serializers.IntegerField(write_only=True)
    product_id = serializers.UUIDField(source="product.id", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_selling_price = serializers.DecimalField(
        source="product.selling_price", max_digits=10, decimal_places=2, read_only=True
    )
    quantity = serializers.IntegerField(min_value=1)

    def validate_product(self, value):
        try:
            ProductService.get_product_by_id(value)
        except:
            raise serializers.ValidationError("Product not found")
        return value

    def validate(self, data):
        product_id = data.get("product_id")
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
