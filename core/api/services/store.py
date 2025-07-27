from django.db import transaction
from django.contrib.auth.models import User
from rest_framework.generics import get_object_or_404
from django.db.models.query import QuerySet
from rest_framework import serializers

from decimal import Decimal
from api.models.store import Product, CartItem


class ProductService:
    @staticmethod
    def get_all_products() -> QuerySet[Product]:
        return Product.objects.all()

    @staticmethod
    def get_product_by_id(product_id: str) -> Product:
        return get_object_or_404(Product, id=product_id)

    @staticmethod
    def check_product_availability(product_id: str, quantity: int) -> bool:
        try:
            product = Product.objects.get(id=product_id)
            return product.inventory_count >= quantity
        except Product.DoesNotExist:
            return False


class CartService:
    @staticmethod
    def get_user_cart(user) -> QuerySet[CartItem]:
        return CartItem.objects.filter(user=user).select_related("product")

    @staticmethod
    def get_cart_item(
        user: User,
        product_id: tuple[str, None] = None,
        item_id: tuple[str, None] = None,
    ) -> CartItem:
        if product_id:
            return get_object_or_404(CartItem, product_id=product_id, user=user)
        return get_object_or_404(CartItem, id=item_id, user=user)

    @staticmethod
    @transaction.atomic
    def add_to_cart(user, product_id: str, quantity: int) -> CartItem:
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found")

        if quantity > product.inventory_count:
            raise serializers.ValidationError(
                f"Quantity ({quantity}) exceeds available stock ({product.inventory_count})"
            )

        cart_item, created = CartItem.objects.get_or_create(
            user=user, product=product, defaults={"quantity": quantity}
        )

        if not created:
            new_quantity = quantity
            if new_quantity > product.inventory_count:
                raise serializers.ValidationError(
                    f"Total quantity ({new_quantity}) exceeds available stock ({product.inventory_count})"
                )
            cart_item.quantity = new_quantity
            cart_item.save()

        return cart_item

    @staticmethod
    @transaction.atomic
    def update_cart_item(user, item_id: str, quantity: int) -> CartItem:
        cart_item = CartService.get_cart_item(user=user, item_id=item_id)
        if quantity > cart_item.product.inventory_count:
            raise serializers.ValidationError(
                f"Quantity ({quantity}) exceeds available stock ({cart_item.product.inventory_count})"
            )

        cart_item.quantity = quantity
        cart_item.save()
        return cart_item

    @staticmethod
    def remove_from_cart(
        user, product_id: tuple[str, None] = None, item_id: tuple[str, None] = None
    ) -> None:
        cart_item = CartService.get_cart_item(
            user=user, item_id=item_id, product_id=product_id
        )
        cart_item.soft_delete()

    @staticmethod
    def get_cart_total(user) -> Decimal:
        cart_items = CartService.get_user_cart(user)
        return sum(item.total_price for item in cart_items)
